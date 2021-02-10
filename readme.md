## 1live-on-spotify
======================
 
## Purpose
Create a spotify playlist based on the songs from Klaus Fiehes show 1LIVE FIEHE (Korrektes Zeug, Raum und Zeit) using spotipy.

## Playlists
If you just want to listen to the songs, you could check out this [overview](https://spty.shell42.de/) or hear the orignal shows at [mixcloud](https://www.mixcloud.com/EinsliveFiehe/) (thx to the unknown uploader).

## Usage
run pip to ensure all requirements are fulfilled
 
```bash
pip3 install -r requirements.txt
```
ensure that you register for a free spotify developers account [here](https://developer.spotify.com/)
and replace the placeholders for SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET with your personal.

now you can run the script by providing an url:
```bash
i.e. main.py -u https://www1.wdr.de/radio/1live/on-air/sendungen/1live-fiehe/index.html
```

## License
This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). <p>
For more details, please take a look at the [LICENSE file](https://github.com/argv1/1live-on-spotify/blob/main/LICENSE).

## Outlook
- [x] Scrap playlist from 1live.de
- [x] Create playlist on spotify based on scraped tracks
- [x] Proccess all [old playlist](http://www.apage4u.de/music/playlist_fiehe.php)

Feel free to adjust the code, things that could be done are:
- [ ] Improving unicode & character encoding
- [ ] Improve the code so that songs from the [missing songs list](https://github.com/argv1/1live-on-spotify/blob/main/missing-tracks.txt) could be added
- [ ] Shazam the songs from the very old shows, somebody provided at [mixcloud](https://www.mixcloud.com/EinsliveFiehe/)


