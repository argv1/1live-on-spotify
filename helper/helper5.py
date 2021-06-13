#!/usr/bin/env python3
'''
    Spotify playlist generator based on the tracks from einslive Klaus Fiehes "Korrektes Zeug"

'''

import pandas as pd
from   pathlib import Path
import spotipy
import spotipy.util as util

# Define path and filename
base_path = Path(__file__).parent.absolute()
SPOTIFY_USERNAME = "SPOTIFY_USERNAME"
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "SPOTIFY_CLIENT_SECRET"
spotify_scope = "playlist-read-private" 
token = util.prompt_for_user_token(username=SPOTIFY_USERNAME, scope=spotify_scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)
 
playlists = sp.user_playlists(SPOTIFY_USERNAME)
df = pd.DataFrame()

while playlists:
    for i, playlist in enumerate(playlists['items']):
        if("1live Fiehe" in playlist['name']):
            df.loc[i + playlists['offset'], "Image"] =  f'<img src="{playlist["images"][0]["url"]}" alt="{playlist["name"]} width="50" height="60">' 
            df.loc[i + playlists['offset'], "Name"] = playlist['name']
            df.loc[i + playlists['offset'], "URL"] = f'<a href="{playlist["external_urls"]["spotify"]}">{playlist["uri"]}</a>'

    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

df.reset_index(drop=True, inplace=True)

# return an html table
pd.set_option('display.max_colwidth', None)
result_file = base_path / "overview.html"

html_table = df.to_html(escape=False)
with open(result_file, "w", encoding="utf-8") as f:
    for line in html_table:
        f.write(line)
