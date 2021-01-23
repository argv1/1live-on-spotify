## 1live-on-spotify
======================
 
## Purpose
Create a spotify playlist based on the songs from Klaus Fiehes show Korrektes Zeug using spotipy.

## Playlists
If you just want to listen to the songs, you could follow me [spotify profile](https://open.spotify.com/user/11123260766) or just visit my [spotify playlists](https://open.spotify.com/playlist/2OS7vZcECoJvIHkp6yedFz).

## Usage
run pip to ensure all requirements are fulfilled
 
```bash
pip3 install -r requirements.txt
```

now you can run the script by providing a new url:
```bash
i.e. main.py -u https://www1.wdr.de/radio/1live/on-air/sendungen/1live-fiehe/index.html
```

## License
This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). <p>
For more details, please take a look at the [LICENSE file](https://github.com/argv1/OReilly-Downloader/blob/master/LICENSE).

## Outlook
- [x] Scrap playlist from 1live.de
- [x] Create playlist on spotify based on scraped tracks
- [ ] Improving unicode & character encoding
- [ ] Fetch all fb posts from Klaus to create playlist for the old 1 Live Fiehe / Raum und Zeit shows

Feel free to adjust the code
