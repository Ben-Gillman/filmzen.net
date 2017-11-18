# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 19:55:15 2017

@author: Ben
"""

import pandas as pd
import sqlite3
import time

def rating_similarity(movie):
    sql_string = "select userId from ratings "\
                 "where liked = 1 and movieId = {};".format(movie)
    liked_movie_users = pd.read_sql_query(sql_string, con)
    liked_movie_users.to_sql("liked_users", con, if_exists="replace", index=False)
    
    sql_string = "select ratings.movieId, ratings.rating from ratings "\
                 "inner join liked_users on liked_users.userId = ratings.userId "\
                 "where ratings.movieId != {};".format(movie)
    liked_movie_rated = pd.read_sql_query(sql_string, con)
    
    liked_movie_rated = liked_movie_rated.groupby('movieId')['rating']\
                                         .agg(['mean','count'])\
                                         .reset_index()
    liked_movie_rated['likedMovie'] = movie
    cols = ['ratedMovie', 'avgRating', 'countRating', 'likedMovie']
    liked_movie_rated = liked_movie_rated.loc[liked_movie_rated['count'] > 30, :]
    liked_movie_rated.columns = cols
    return liked_movie_rated


def get_genomes(movie):
    sql_string = "select * from genome_similarity where movieId2 = {};".format(movie)
    return pd.read_sql_query(sql_string, con)


def calculate_scores(ratings, genomes, movies_master, num_top=10):
    scores = pd.merge(ratings, genomes, how='left', 
                      left_on=['ratedMovie', 'likedMovie'], 
                      right_on=['movieId', 'movieId2'])
    
    scores['score'] = scores.avgRating / (scores.avgRating.max() * 10) + scores.similarity
    max_score = scores['score'].max()
    scores['score'] = max_score - scores['score']
    scores = pd.merge(scores, movies_master[['title', 'movieId']], 
                      left_on='ratedMovie', right_on='movieId')
    scores = scores[["likedMovie", "ratedMovie", "title", "avgRating", 
                     "countRating", "similarity", "score"]]
    return scores.sort_values('score', ascending=True)\
                 .head(num_top)\
                 .loc[:,'title']\
                 .values

if __name__ == '__main__':
    con = sqlite3.connect("C:\\Users\Ben\Documents\movie_recs\data.sqlite3")
    movies_master = pd.read_sql_query("select * from movie_master;", con)
    
    # Get a movie id from user
    movie = 1

    start_time = time.time()
    liked_rated = rating_similarity(movie)
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")

    start_time = time.time()    
    genome_similarity = get_genomes(movie)
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")

    start_time = time.time()    
    title = movies_master.loc[movies_master['movieId']==movie, 'title'].values[0]
    print("Top movies for {}:".format(title))
    print(calculate_scores(liked_rated, genome_similarity, movies_master))
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")
    
    