import requests
import bs4
import pandas as pd

def get_imdb_link(movieId, con):
    sql_string = "select imdbId from movie_master where movieId={}".format(movieId)
    imdbId = pd.read_sql_query(sql_string, con)
    return imdbId.values[0][0]


def get_movie_poster_links(imdbIdContainer):
    linkContainer = []

    for imdbId in imdbIdContainer:
        id_string = str(imdbId).zfill(7)
        movie_link = "http://www.imdb.com/title/tt" + id_string + "/"
        response = requests.get(movie_link)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        img_link = soup.select(".poster img")[0].attrs['src']
        linkContainer.append(img_link)

    return linkContainer
