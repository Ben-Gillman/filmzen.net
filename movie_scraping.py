import requests
import bs4
import pandas as pd
import json 

def get_imdb_link(movieId, con):
    sql_string = "select imdbId from movie_master where movieId={}".format(movieId)
    imdbId = pd.read_sql_query(sql_string, con)
    return imdbId.values[0][0]


def get_media_links(imdbIdContainer):
    link_container = []

    for imdbId in imdbIdContainer:
        movie_container = []

        # Get movie poster
        id_string = str(imdbId).zfill(7)
        movie_link = "http://www.imdb.com/title/tt" + id_string + "/"
        response = requests.get(movie_link)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        img_link = soup.select(".poster img")[0].attrs['src']

        movie_container.append(img_link)

        # Get trailer 
        try:
            playlist_link = soup.select(".slate a")[0].attrs['data-video']
            playlist_link = movie_link + "videoplayer/" + playlist_link

            response = requests.get(playlist_link)
            resp_text = response.text

            json_key = "window.IMDbReactInitialState.push("
            index_1 = resp_text.find(json_key)
            index_2 = resp_text.find(");", index_1)
            page_json = resp_text[index_1 + len(json_key):index_2]

            page_data = json.loads(page_json)
            video_key = page_data["videos"]["playlists"].keys()
            video_key = [s for s in video_key if "vi" in s][0]
            video_link = list(page_data["videos"]["videoMetadata"][video_key]["encodings"])\
                         [0]["videoUrl"]
        except:
            video_link = None

        movie_container.append(video_link)
        link_container.append(movie_container)


    return link_container

