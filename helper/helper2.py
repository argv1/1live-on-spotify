#!/usr/bin/env python3
'''
    Small helper script to create csv playlist files based on last years 1live playlist and directly create the spotify playlist.

'''
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import pandas as pd
from   pathlib import Path
import re
import requests
import spotipy
import spotipy.util as util

# Define path and filename
base_path = Path(__file__).parent.absolute()
playlists = base_path / "playlists"
base_url = "https://www1.wdr.de/radio/1live/on-air/sendungen/1live-fiehe/fiehe-"
SPOTIFY_USERNAME = "SPOTIFY_USERNAME"
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "SPOTIFY_CLIENT_SECRET"
spotify_scope = "playlist-modify-public" 
token = util.prompt_for_user_token(username=SPOTIFY_USERNAME, scope=spotify_scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)
playlist_description = f"Created by argv1 https://github.com/argv1/1live-on-spotify"

def get_track_ids(df):
    # Get Spotify track ids for the playlist
    track_ids, track_ids_not_found = [], []
    # Track Info Box Flow
    for i in range(len(df)):
        results = sp.search(q=f"{df['Titel'][i]} {df['Interpret'][i]} ", limit=5, type='track')
        # if track isn't on spotify as queried, go to next track
        if results['tracks']['total'] == 0: 
            continue
        else:
            for j in range(len(results['tracks']['items'])):
                # Get right response by matching on artist and title
                if fuzz.partial_ratio(results['tracks']['items'][j]['artists'][0]['name'], df['Interpret'][i]) > 90 and fuzz.partial_ratio(results['tracks']['items'][j]['name'], df['Titel'][i]) > 90 : 
                    track_ids.append(results['tracks']['items'][j]['id']) 
                    break
                else:
                    track_ids_not_found.append((f"{df['Titel'][i]} from {df['Interpret'][i]}"))
                    continue
    print(f"The following tracks could not be found on spotify: {set(track_ids_not_found)}")
    return track_ids

def get_playlist_id(playlist_name):
    playlists = sp.user_playlists(SPOTIFY_USERNAME)
    # iterate through spotify_username playlists
    for playlist in playlists['items']:
        # filter for newly created playlist
        if playlist['name'] == playlist_name:  
            return(playlist['id'])

def generate_playlist(df, date): 
    # Create playlist
    playlist_name = f"1live Fliehe vom {date}"    
    sp.user_playlist_create(user=SPOTIFY_USERNAME, name=playlist_name, description=playlist_description)

    # Get Tracks
    track_ids = get_track_ids(df)

    # Remove duplicate tracks order preserving  
    track_ids = list(dict.fromkeys(track_ids))
    playlist_id = get_playlist_id(playlist_name)

    # Populate playlist
    sp.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, track_ids)

def get_tracks(page):
    try:
        content = requests.get(f"{base_url}{page}.html")
        date = re.findall(r'<table class="thleft"><caption>Playlist der Sendung vom (\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*)', content.text)
        filename = f"{date[0][3]}-{date[0][2]}-{date[0][1]}"

        tab_list = pd.read_html(content.content)
        df = tab_list[0]
        df.dropna(axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f"{playlists}/{filename}.csv", index=False, sep=";", encoding="iso-8859-1")
    except:
        print(f"{page} does not exists.")
        return('test', 'test', False)
    return(df, filename, True)

def main():
    for page in range(704,708,2):   
        df, date, check = get_tracks(page)
        if(check):
            # Remove unnecessary whitespaces
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
                                  
            generate_playlist(df, date)
            print(f"Playlist für {page} {date} erfolgreich\n.")
        
if __name__  == "__main__":
    main()
