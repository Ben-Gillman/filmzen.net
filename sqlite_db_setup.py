# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 21:05:10 2017

@author: Ben

Create non-user generated tables in the sqlite database
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import sqlite3

# Reverse ","" endings on movie names  
def movie_name_cleanup(movie_name):
    if movie_name.endswith(", A"):
        movie_name = movie_name[-1] + " " + movie_name[:-3]
    elif movie_name.endswith((", The", ", Les")):
        movie_name = movie_name[-3:] + " " + movie_name[:-5]
    elif movie_name.endswith(", An"):
        movie_name = movie_name[-2:] + " " + movie_name[:-4]
    elif movie_name.endswith(", L'"):
        movie_name = movie_name[-2:] + movie_name[:-4]        
    return movie_name

data_dir = r"C:\Users\Ben\Documents\Data Sets\movielens_20m_dataset\\"


# Read in data 
movies_master = pd.read_csv(data_dir+"movie.csv")
ratings = pd.read_csv(data_dir+"rating.csv")
genome_scores = pd.read_csv(data_dir+'genome_scores.csv')
link = pd.read_csv(data_dir+"link.csv")


# Import and clean up movies master 
movies_master["year"] = movies_master.title.str[-6:]\
                                     .str.extract('(\d+)', expand=False)\
                                     .astype(float)
movies_master["title"] = movies_master["title"].apply(lambda x: x.split("(")[0][:-1])
movies_master["title"] = movies_master["title"].apply(movie_name_cleanup)

# Find and filter out unpopular movies 
popular_movies = ratings.groupby("movieId")\
                        .userId\
                        .count()\
                        .reset_index()
popular_movies.columns = ['movieId', 'num_user']
popular_movies = popular_movies.sort_values("num_user", ascending=False)
popular_movies = popular_movies[popular_movies.num_user > 30]

ratings = ratings[ratings["movieId"].isin(popular_movies["movieId"])]
movies_master = movies_master[movies_master["movieId"]\
                              .isin(popular_movies["movieId"])]

# add imdb link to movies master
movies_master = pd.merge(movies_master, link.iloc[:,0:2], on="movieId")

# Assign movies that were "liked" by users
quartiles = ratings.groupby("movieId")\
                   .rating\
                   .quantile(q=.8, interpolation='midpoint')\
                   .reset_index()
quartiles.columns = ["movieId", "top_quintile"]
ratings = pd.merge(ratings, quartiles, on = "movieId")
ratings['liked'] = np.where(ratings['rating'] >= ratings['top_quintile'], 1, 0)


# Calculate movie tag similarity
genome_scores = pd.pivot_table(genome_scores, 
                               values='relevance', 
                               index='movieId', 
                               columns='tagId')\
                               .reset_index()
genome_scores = genome_scores[genome_scores['movieId'].isin(movies_master['movieId'])]
genome_similarity = cosine_similarity(genome_scores.iloc[:,1:])
tagged_movieIds = list(genome_scores['movieId'])
genome_similarity = pd.DataFrame(genome_similarity, columns=tagged_movieIds)
genome_similarity['movieId'] = [int(mov) for mov in tagged_movieIds]
genome_similarity = genome_similarity.melt(id_vars='movieId', var_name='movieId2', value_name='similarity')
genome_similarity = genome_similarity[genome_similarity.movieId != genome_similarity.movieId2]


# Send dataframes to SQLite3 database 
con = sqlite3.connect("C:\\Users\Ben\Documents\movie_recs\data.sqlite3")

movies_master.to_sql("movie_master", con, if_exists="replace", index=False)
genome_similarity.to_sql("genome_similarity", con, if_exists="replace", index=False)
ratings.to_sql("ratings", con, if_exists="replace", index=False)

pd.read_sql_query("select * from movie_master LIMIT 20;", con)
pd.read_sql_query("select * from ratings LIMIT 20;", con)
pd.read_sql_query("select * from genome_similarity LIMIT 20;", con)


# Create result_cache table 
sql_string = "CREATE TABLE IF NOT EXISTS result_cache ("\
             "likedMovie integer," \
             "ratedMovie integer," \
             "title text);"

cursor.execute(sql_string)
