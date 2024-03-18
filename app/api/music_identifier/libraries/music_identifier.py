from app.utils.response import MusicTrainResponse
import librosa
import numpy as np
import sqlite3
from datetime import datetime
import time
    
conn = sqlite3.connect("songs.db")
cur = conn.cursor()    
    
async def train_music(sound):
    create_table()
    
    # Generate unique name for the music with timestamp
    # timestamp = time.time() + datetime.timedelta()
    # print(timestamp)
    # music_name = f"music{music.uploader_id}_{timestamp}"
    # with open(f"music/{music.name}.mp3", "wb") as f:
    #     f.write(contents)
    # Training Steps
    music_details = {}
    if music_details:
        return MusicTrainResponse(
            code=200,
            response="Music Trained",
            data=music_details
        )
    else:
        return MusicTrainResponse(
            code=404,
            response="Music is Not Trained",
            data=None
        ) 
    
def create_table():
  cur.execute('''CREATE TABLE IF NOT EXISTS songs (
                name TEXT PRIMARY KEY,
                fingerprint BLOB
                )''')
  conn.commit()

def add_song(song_name, audio_path):
  # Load audio data
  y, sr = librosa.load(audio_path)

  # Extract MFCCs
  mfccs = librosa.feature.mfcc(y=y, sr=sr)

  # Generate fingerprint (using mean MFCCs for simplicity)
  fingerprint = np.mean(mfccs.T, axis=0)

  # Insert fingerprint and name into database
  cur.execute("INSERT OR IGNORE INTO songs (name, fingerprint) VALUES (?, ?)", (song_name, fingerprint.tobytes()))
  conn.commit()
  print(f"Song '{song_name}' added to database.")

def identify_song(audio_path):
  """
  This function identifies a song based on its fingerprint and calculates similarity.
  """
  # Load audio data
  y, sr = librosa.load(audio_path)

  # Extract MFCCs
  mfccs = librosa.feature.mfcc(y=y, sr=sr)

  # Generate fingerprint
  fingerprint = np.mean(mfccs.T, axis=0)

  # Convert fingerprint to byte array for database comparison
  fingerprint_bytes = fingerprint.tobytes()

  # Retrieve all songs from database
  cur.execute("SELECT * FROM songs")
  songs = cur.fetchall()

  # Compare fingerprint with all songs in database (replace with more efficient methods for larger databases)
  best_match = None
  best_distance = float("inf")
  for song_name, db_fingerprint in songs:
    distance = np.linalg.norm(np.frombuffer(db_fingerprint, dtype=np.float32) - fingerprint)
    if distance < best_distance:
      best_match = song_name
      best_distance = distance

  # Calculate similarity percentage
  similarity = 1 / (1 + best_distance) * 100

  if best_match:
    print(f"Most similar song: {best_match} (Similarity: {similarity:.2f}%)")
  else:
    print("No matching songs found in database.")

  return best_match, similarity
    
        
async def identify_music(music, file):
    contents = await file.read()
    
    # Identification Steps
    music_details = {}
    if music_details:
        return MusicTrainResponse(
            code=200,
            response="Music Identified",
            data=music_details
        )
    else:
        return MusicTrainResponse(
            code=404,
            response="Music is Not Identified",
            data=None
        )
        
        
async def get_music_data(music):
    # Get Music Data
    music_details = {}
    if music_details:
        return MusicTrainResponse(
            code=200,
            response="Music Data Retrieved",
            data=music_details
        )
    else:
        return MusicTrainResponse(
            code=404,
            response="Music Data Not Retrieved",
            data=None
        )