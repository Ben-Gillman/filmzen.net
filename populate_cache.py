# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 11:09:32 2018

@author: Ben
"""
if __name__ == '__main__':    
    import movie_recommendation_engine as movrec
    import movie_scraping as movscrp
    import movie_caching as movcache
    
    from flask_sqlalchemy import SQLAlchemy
    from flask import Flask
    from config import Config
    from flask_bootstrap import Bootstrap
    
    import pandas as pd
    import sqlite3
    import time
    
    app = Flask(__name__)
    app.config.from_object(Config)
    bootstrap = Bootstrap(app)
    db = SQLAlchemy(app)
    
    con = sqlite3.connect("C:\\Users\Ben\Documents\movie_recs\data.sqlite3")
    cursor = con.cursor()
    
    movies = pd.read_sql_query("SELECT movieId from movie_master", con)
    
    start_time = time.time()
    for movie_id in movies.values[155:300]:
        movie_id = movie_id[0] 
        print(movie_id)
    
        liked_rated = movrec.rating_similarity(movie_id, db.get_engine())
        genome_similarity = movrec.get_genomes(movie_id, db.get_engine())
        top_movies = movrec.calculate_scores(liked_rated, genome_similarity, db.get_engine())
        if len(top_movies) < 3:
            continue
        imdb_media = movscrp.get_media_links(top_movies['imdbId'])
        top_movies = pd.concat([top_movies, imdb_media], axis=1)
        top_movies = top_movies.drop('index', 1)
        movcache.cache_result(top_movies, db.get_engine())
        print(movie_id, "is done")
    print("This cell took", (time.time() - start_time) / 60, "minutes to run")