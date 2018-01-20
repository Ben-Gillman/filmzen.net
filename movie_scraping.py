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
        movie_description = None

        # Get movie poster
        id_string = str(imdbId).zfill(7)
        movie_link = "http://www.imdb.com/title/tt" + id_string + "/"
        response = requests.get(movie_link)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        img_link = soup.select(".poster img")[0].attrs['src']

        movie_container.append(img_link)

        # Get trailer 
        playlist_link = soup.select(".slate a")
        if playlist_link:
            playlist_link = playlist_link[0].attrs['data-video']
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
        else:
            playlist_link = soup.select(".video_slate_last a")
            if playlist_link:
                playlist_link = playlist_link[0].attrs['data-video']
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
            else:
                video_link = None
                movie_description = soup.select(".summary_text")[0].text

        movie_container.append(video_link)
        movie_container.append(movie_description)
        link_container.append(movie_container)


    return link_container

