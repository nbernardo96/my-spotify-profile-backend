from flask import request
from app import app
import lyricsgenius
from random import *
import os


@app.route("/api/home")
def index():
  return 'Home'

@app.route("/api/lyrics")
def get_lyrics():
  GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')
  genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

  artist = request.args.get('artist')
  title = request.args.get('title')
  song = genius.search_song(title, artist)
  
  if song and 'Chorus' in song.lyrics:
    song_parts = song.lyrics.split('\n\n')
    filters = ['Verse 1', 'Verse 2', 'Chorus', 'Bridge', 'Pre-Chorus']
    lyrics = []

    for p in song_parts:
        if 'Verse 1' in p or 'Verse 2' in p or 'Chorus' in p or 'Bridge' in p or 'Pre-Chorus' in p:
            part = p.split('\n')
            lyrics.extend(part)
    
    lyrics_filtered = [l for l in lyrics if not any(f in l for f in filters)]
    start = randint(0, len(lyrics_filtered) - 4)
    stop = start + 4
    
    randomized_lyric = (lyrics_filtered[start:stop])
    return randomized_lyric, 200
  return '', 400
