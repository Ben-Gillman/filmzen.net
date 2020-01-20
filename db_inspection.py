# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 19:06:37 2017

@author: Ben

Inspecting / Creating SQLite3 database for flask application
"""
import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Inspect Tables
con = sqlite3.connect("C:\\Users\Ben\Documents\movie_recs\data.sqlite3")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

df = pd.read_sql_query("SELECT * from user_input", con)
df2 = pd.read_sql_query("SELECT * from user_feedback", con)



# Create table example 
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

# Clear the cache
sql_string = "DELETE FROM result_cache;"
cursor.execute(sql_string)
cursor.execute("SELECT * FROM result_cache;")
print(cursor.fetchall())

# Drop a table 
sql_string = "DROP TABLE result_cache;"
cursor.execute(sql_string)

# close connection to the db
cursor.close()
con.close()
