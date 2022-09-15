# Bot to help create playlist on spotify from songs on Bill board 100 for any year!!

# import requests, spotipy, beautiful soup
import spotipy as spotipy
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# You will need to insert your own client ID, Client secret and Redirect UI's on spotipy
# You can use this link to get started on getting your own: 'https://spotipy.readthedocs.io/en/master/'
CLIENT_ID=""
CLIENT_SECRET=""
REDIRECT_UIs=""

# Get songs from billboard chart using beautiful soup
# Beautiful soup documentation can be found here: 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
URL="https://www.billboard.com/charts/hot-100/"
date =input("Which year do you ant to travel to? Type the date in this format :YYYY-MM-DD:")
response=requests.get(URL+date)
html_doc=response.content
soup = BeautifulSoup(html_doc, 'html.parser')
song_tiltles=[link.find("h3",id='title-of-a-story').text.strip() for link in soup.find_all('div',"o-chart-results-list-row-container")]

# Open spotipy using Client ID,Client ID, and Redirect url
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_UIs,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

# Get user ID, information on this can be found in spotipy documentation
user_id = sp.current_user()["id"]

song_uris=[]
year=date.split("-")[0]
# Search for song on spotify , if song exists, store song info in list, if it doesn't skip song
for song in song_tiltles:
    result=sp.search(q=f"track:{song} year:{year}",type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#Create and add playlist to spotify
playlist=sp.user_playlist_create(user=user_id,name=f"{date} Billboard chart playlist",public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)