#!/usr/bin/env python3
'''
    Small helper script to create spotify playlist for every csv file in the playlist folder.

'''
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from os import listdir
import pandas as pd
from   pathlib import Path
import re
import requests
import spotipy
import spotipy.util as util
import sys

# Define path and filename
base_path = Path(__file__).parent.absolute()
playlists = base_path / "playlists"
SPOTIFY_USERNAME = "SPOTIFY_USERNAME"
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "SPOTIFY_CLIENT_SECRET"
spotify_scope = "playlist-modify-public" 
token = util.prompt_for_user_token(username=SPOTIFY_USERNAME, scope=spotify_scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost/:8080')
sp = spotipy.Spotify(auth=token)
playlist_description = f"Klaus Fiehes weekly 1live show, formaly known as Raum und Zeit             Created by argv1 https://github.com/argv1/1live-on-spotify"

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

def main():
    for entry in listdir(playlists):
        filename = playlists / entry
        date = entry[:-4]
        try:
            df = pd.read_csv(filename, delimiter=";", encoding="cp1252")
        except:
            df = pd.read_csv(filename, delimiter=";", encoding="utf-8")

        # Remove unnecessary whitespaces
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)                                       
                                                
        generate_playlist(df, date)
        print(f"Playlist für {date} erfolgreich\n.")
        
if __name__  == "__main__":
    main()