#!/usr/bin/env python3
'''
    Small helper script to create csv playlist files based on the current 1live FLIEHE show.
'''
import pandas as pd
from pathlib import Path
import re
import requests

# Define path and filename
base_path = Path(__file__).parent.absolute()
playlists = base_path / "playlists"
fetched_shows = playlists / "fetched_shows.csv"
base_url = "https://www1.wdr.de/radio/1live/on-air/sendungen/1live-fiehe/"


def get_tracks():
    try:
        content = requests.get(base_url)
    except:
        print(f"Site does not exists.")

    date = re.findall(r'<table class="thleft"><caption>1LIVE Fiehe - Playlist der Sendung vom (\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*)',content.text)
    filename = f"{date[0][3]}-{date[0][2]}-{date[0][1]}"

    tab_list = pd.read_html(content.content)
    df = tab_list[0]
    df.dropna(axis=0, inplace=True)
    try:
        df.to_csv(f"{playlists}/{filename}.csv", index=False, sep=";", encoding="cp1252")
    except:
        df.to_csv(f"{playlists}/{filename}.csv", index=False, sep=";", encoding="utf-8")

def main():
    get_tracks()

if __name__ == "__main__":
    main()