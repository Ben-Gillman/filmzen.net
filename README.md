# [Filmzen.net](http://filmzen.net/)

## What 

FilmZen keeps you calm in the storm of movie recommendations provided by streaming services.

Watch your next favorite movie with FilmZen. Enter a movie and receive three recommendations based off of that movie. Movies are recommended based on the movie's attributes and the preferences of those who also liked the movie you entered. Only relatively popular movies that came out before March 2015 are in the data set.

The data used to make the recommendations comes from GroupLens.org1. Recommendations are a weighted average of two metrics. The first is the average rating given to movies by those who also liked the entered movie. The second metric is the cosine similarity between the tags given to the movie and tags assigned to all 27,000 movies in the dataset.

## Getting Started

movie_recs.py is the main file of the flask-based website

Wesbite database was built using Movie Data Analysis.ipynb and is not included in this repo due to its size

##### Data comes from F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages. DOI=http://dx.doi.org/10.1145/2827872
