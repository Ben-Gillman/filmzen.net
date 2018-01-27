import requests
import bs4
import json 

imdbId = 77975 # movie to lookup

id_string = str(imdbId).zfill(7)
movie_link = "http://www.imdb.com/title/tt" + id_string + "/"
response = requests.get(movie_link)
soup = bs4.BeautifulSoup(response.text, "lxml")

# Grab img
img_link = soup.select(".poster img")[0].attrs['src']


# Grab playlist URL
try:
    playlist_link = soup.select(".slate a")
except:
    try:
        playlist_link = soup.select(".video_slate_last a")[0].attrs['data-video']
    except:
        playlist_link = "vi126484761"
        
playlist_link = movie_link + "videoplayer/" + playlist_link
#playlist_link = movie_link + "videoplayer/vi126484761"

# Grab JSON containing video 
response = requests.get(playlist_link)  
resp_text = response.text

# Grab video from Json
json_key = "window.IMDbReactInitialState.push("
index_1 = resp_text.find(json_key)
index_2 = resp_text.find(");", index_1)
page_json = resp_text[index_1 + len(json_key):index_2]

page_data = json.loads(page_json)
video_key = page_data["videos"]["playlists"].keys()
video_key = [s for s in video_key if "vi" in s][0]
video_link = list(page_data["videos"]["videoMetadata"][video_key]["encodings"])\
             [0]["videoUrl"]

# Grab movie description text
movie_summary = soup.select(".summary_text")[0].text
           
             
#<a href="/title/tt0111257/videoplayer/vi126484761?ref_=tt_pv_vi_aiv_1" title="Speed -- Pre, &quot;June 10th&quot;" alt="Speed -- Pre, &quot;June 10th&quot;" class="video-modal" data-video="vi126484761" data-context="screenplay" data-rid="0RCVN7CD49SGWGPY75PA" widget-context="titleMaindetails" itemprop="url"><img height="105" width="139" alt="Speed -- Pre, &quot;June 10th&quot;" title="Speed -- Pre, &quot;June 10th&quot;" src="https://images-na.ssl-images-amazon.com/images/M/MV5BMjEwMjM0NjE2Nl5BMl5BanBnXkFtZTcwNTgxNjc2MQ@@._V1_SP229,229,0,C,0,0,0_CR45,62,139,105_PIimdb-blackband-204-14,TopLeft,0,0_PIimdb-blackband-204-28,BottomLeft,0,1_CR0,0,139,105_PIimdb-bluebutton-big,BottomRight,-1,-1_ZATrailer,2,76,16,137,verdenab,8,255,255,255,1_ZAon%2520IMDb,2,1,14,137,verdenab,7,255,255,255,1_ZA02%253A37,103,1,14,36,verdenab,7,255,255,255,1_.jpg" class="loadlate video" itemprop="image" viconst="vi126484761"></a>