#!/usr/bin/env python3
'''
    Spotify playlist generator based on the tracks from einslive Klaus Fiehes "Korrektes Zeug"
    Created by argv1 https://github.com/argv1/1live-on-spotify
'''
import argparse
from configparser import ConfigParser
from fuzzywuzzy import fuzz, process
import pandas as pd
from pathlib import Path
import re
import requests
import spotipy
import spotipy.util as util

def get_track_ids(df):
    # Get Spotify track ids for the playlist
    track_ids, track_ids_not_found = [], []
    # Track Info Box Flow
    for i in range(len(df)):
        results = sp.search(q=f"{df['Artist'][i]} {df['Track'][i]} ", limit=5, type='track')
        # if track isn't on spotify as queried, go to next track
        if results['tracks']['total'] == 0: 
            continue
        else:
            for j in range(len(results['tracks']['items'])):
                # Get right response by matching on artist and title
                if fuzz.partial_ratio(results['tracks']['items'][j]['artists'][0]['name'], df['Artist'][i]) > 90 and fuzz.partial_ratio(results['tracks']['items'][j]['name'], df['Track'][i]) > 90 : 
                    track_ids.append(results['tracks']['items'][j]['id']) 
                    break
                else:
                    track_ids_not_found.append((f"{df['Track'][i]} from {df['Artist'][i]}"))
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
    playlist_name = f"1live Klaus Fliehe vom {date}"
    sp.user_playlist_create(user=SPOTIFY_USERNAME, name=playlist_name, description=playlist_description)

    # Get Tracks
    track_ids = get_track_ids(df)

    # Remove duplicate tracks order preserving  
    track_ids = list(dict.fromkeys(track_ids))
    playlist_id = get_playlist_id(playlist_name)

    # Populate playlist
    sp.playlist_add_items(playlist_id, track_ids)

def get_tracks(url):
    try:
        content = requests.get(f"{url}")
    except:
        print(f"{url} does not exists.")

    date = re.findall(r'<table class="thleft"><caption>1LIVE Fiehe - Playlist der Sendung vom (\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*)',content.text)
    filename = f"{date[0][3]}-{date[0][2]}-{date[0][1]}"

    tab_list = pd.read_html(content.content)
    df = tab_list[0]
    df.dropna(axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    try:
        df.to_csv(f"{playlists}/{filename}.csv", index=False, sep=";", encoding="cp1252")
    except:
        df.to_csv(f"{playlists}/{filename}.csv", index=False, sep=";", encoding="utf-8")

    return(df, filename)

def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Enter the url of the show that should be scrapped', type=str, default="https://www1.wdr.de/radio/1live/on-air/sendungen/1live-fiehe/")
    args = parser.parse_args()
    df, date = get_tracks(args.url)

    # Remove unnecessary whitespaces
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    generate_playlist(df, date)
        
if __name__  == "__main__":
    # Global settings
    base_path = Path(__file__).parent.absolute()
    playlists = base_path / "playlists"
    config_file = ConfigParser()
    config_file.read(base_path / 'config.ini')
    SPOTIFY_USERNAME = config_file['AUTH']['SPOTIFY_USERNAME']
    SPOTIFY_CLIENT_ID = config_file['AUTH']['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = config_file['AUTH']['SPOTIFY_CLIENT_SECRET']
    spotify_scope = "playlist-modify-public" 
    token = util.prompt_for_user_token(username=SPOTIFY_USERNAME, scope=spotify_scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:8888/callback')
    sp = spotipy.Spotify(auth=token)
    playlist_description = f"Created by argv1 https://github.com/argv1/1live-on-spotify"
    
    main()
