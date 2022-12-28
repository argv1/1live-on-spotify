#!/usr/bin/env python3
'''
    Spotify playlist mass renaming (description)

'''
import spotipy
import spotipy.util as util

# Define path and filename
SPOTIFY_USERNAME = "SPOTIFY_USERNAME"
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "SPOTIFY_CLIENT_SECRET"
spotify_scope = "playlist-modify-public" 
token = util.prompt_for_user_token(username=SPOTIFY_USERNAME, scope=spotify_scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)
playlist_description = f"Klaus Fiehes weekly 1live show, formaly known as Raum und Zeit             Created by argv1 https://github.com/argv1/1live-on-spotify" 
playlists = sp.user_playlists(SPOTIFY_USERNAME)

while playlists:
    for i, playlist in enumerate(playlists['items']):
        if("1live Klaus Fliehe" in playlist['name']):
            playlist_name = "1live F" + playlist['name'][8:]
            sp.playlist_change_details(playlist_id=playlist['id'], name=playlist_name, public=True, collaborative=None, description=playlist_description)
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None