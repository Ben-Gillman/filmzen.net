# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 19:06:37 2017

@author: Ben

Inspecting / Creating SQLite3 database for flask application
"""
import pandas as pd
import sqlite3

# Inspect Tables
con = sqlite3.connect("C:\\Users\Ben\Documents\movie_recs\data.sqlite3")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

df = pd.read_sql_query("SELECT * from user_input", con)



# Create tables
