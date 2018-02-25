# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 11:50:41 2018

@author: Ben
"""
if __name__ == '__main__':
    import sqlite3
    
    # Inspect Tables
    con = sqlite3.connect("C:\\Users\Ben\Documents\movie_recs\data.sqlite3")
    cursor = con.cursor()
    
    sql_string = "DELETE FROM result_cache;"
    cursor.execute(sql_string)
    
    sql_string = "CREATE TABLE IF NOT EXISTS result_cache ("\
                 "likedMovie integer," \
                 "ratedMovie integer," \
                 "title text," \
                 "linkTitle text,"\
                 "imdbId integer,"\
                 "imdbPoster text,"\
                 "imdbTrailer text,"\
                 "imdbDesc text);"
    cursor.execute(sql_string)
    
    cursor.execute("SELECT * FROM result_cache;")
    print("cache contains:" , cursor.fetchall())