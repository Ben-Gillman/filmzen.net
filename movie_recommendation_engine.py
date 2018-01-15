# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 19:55:15 2017

@author: Ben
"""

import pandas as pd
import time
from fuzzywuzzy import process, fuzz
import movie_scraping as movscrp


# gets movie id from given movie name 
def get_movie_id(movie_name, con):
    sql_string = "select movieId, title from movie_master;"
    movie_master = pd.read_sql_query(sql_string, con)
    # TODO if no movie is found, prompt the user for another name 
    movie_name = process.extractOne(movie_name.lower(), 
                                    movie_master.iloc[:,1].str.lower(), 
                                    scorer=fuzz.ratio,
                                    score_cutoff=20)[0]
    if movie_name == None: return -1

    movieId = movie_master.loc[movie_master.loc[:,'title'].str.lower()==movie_name,'movieId']\
                          .values[0]
    return movieId


# Use movieId to find the proper name of a movie 
def get_print_movie_name(movieId, con):
    sql_string = "select title from movie_master where movieId = {};".format(movieId)
    movie_name = pd.read_sql_query(sql_string, con)
    return movie_name.values[0][0]


# Gets rating of movies thats other people liked who also liked given movie
def rating_similarity(movie, con):
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


# Get genome scores for all movies compared to given movie
def get_genomes(movie, con):
    sql_string = "select * from genome_similarity where movieId2 = {};".format(movie)
    return pd.read_sql_query(sql_string, con)


def append_imdbIds(top_movies, con):
    imdbIdContainer = []

    for ratedMovie in top_movies.loc[:,'ratedMovie']:
        imdbId = movscrp.get_imdb_link(ratedMovie, con)
        print(imdbId)
        imdbIdContainer.append(imdbId)

    top_movies = top_movies.assign(imdbId=imdbIdContainer)
    return top_movies


# Calculates similarity scores given genome and rating scores 
def calculate_scores(ratings, genomes, con, num_top=10):
    movie_master = pd.read_sql_query("select * from movie_master;", con)

    scores = pd.merge(ratings, genomes, how='left', 
                      left_on=['ratedMovie', 'likedMovie'], 
                      right_on=['movieId', 'movieId2'])
    
    scores['score'] = scores.avgRating / (scores.avgRating.max() * 10) + scores.similarity
    max_score = scores['score'].max()
    scores['score'] = max_score - scores['score']
    scores = pd.merge(scores, movie_master[['title', 'movieId']], 
                      left_on='ratedMovie', right_on='movieId')
    scores = scores[["likedMovie", "ratedMovie", "title", "avgRating", 
                     "countRating", "similarity", "score"]]
    scores = scores.sort_values('score', ascending=True)\
                   .drop_duplicates(subset=["title"])
    scores = scores.head(num_top)\
                 .loc[:,["likedMovie","ratedMovie","title"]]
    return append_imdbIds(scores, con)


if __name__ == '__main__':
    from flask import Flask
    from flask_bootstrap import Bootstrap
    from flask_wtf import FlaskForm
    from wtforms import StringField, SubmitField
    from wtforms.validators import Required, Length
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'top secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bootstrap = Bootstrap(app)
    db = SQLAlchemy(app)

    # Get a movie id from user
    movie = 1

    start_time = time.time()
    liked_rated = rating_similarity(movie, db.get_engine())
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")

    start_time = time.time()    
    genome_similarity = get_genomes(movie, db.get_engine())
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")

    start_time = time.time()    
    movie_master = pd.read_sql_query("select * from movie_master;", db.get_engine())
    title = movie_master.loc[movie_master['movieId']==movie, 'title'].values[0]
    print("Top movies for {}:".format(title))
    top_movies = calculate_scores(liked_rated, genome_similarity, db.get_engine())
    print(type(top_movies)) 
    # print(top_movies[0])
    # print(top_movies[1])
    # print(calculate_scores(liked_rated, genome_similarity, db.get_engine()))
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")
    