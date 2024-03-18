from app.utils.response import MusicTrainResponse, MusicResponseModel
import librosa
import numpy as np
import sqlite3
import datetime
import time
import os
from app.api.music_identifier.libraries import support
from app.utils.database import music_collection
from app.models.MusicIdentifier import MusicNew, MusicResponse
from bson import ObjectId


from app.utils.logging import get_logger
logger = get_logger()  
    
DB_FILE = "app/data/music.db"
    
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()    
UPLOAD_DIR = "app/temp/songs/"

async def train_music(file, song_name, user_id):
    create_table()
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generat eunique name
    unique_name = str(int(time.time()))
    file_path = f"{os.path.join(UPLOAD_DIR, unique_name)}.mp3"
    with open(f"{file_path}", "wb") as buffer:
        buffer.write(file.file.read())
    
    music_details = {}
    
    platform_name = "Radio King"
    music_details['title'] = str(song_name)
    music_details['user_id'] = str(user_id)
    music_details['type'] = 'music'
    music_details['total_stream'] = "0"
    music_details['total_platform'] = "1"
    music_details['total_time'] = "0"
    
    
    platform_records = [
        {
            'platform_name': platform_name,
            'stream_count': "0",
            'records': []
        }
    ]
    music_details['platform_details'] = platform_records
    
    musics = music_collection.insert_one(music_details)
    if musics.inserted_id:
        add_song(str(musics.inserted_id), file_path)
    
    if music_details:
        return MusicTrainResponse(
            code=200,
            response="Music Trained",
            data=MusicNew(id=str(musics.inserted_id))
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
    
  y, sr = librosa.load(audio_path)
  mfccs = librosa.feature.mfcc(y=y, sr=sr)
  fingerprint = np.mean(mfccs.T, axis=0)

  cur.execute("INSERT OR IGNORE INTO songs (name, fingerprint) VALUES (?, ?)", (song_name, fingerprint.tobytes()))
  conn.commit()
  logger.info(f"Song '{song_name}' added to database.")

def identify_song(audio_path):
  y, sr = librosa.load(audio_path)
  mfccs = librosa.feature.mfcc(y=y, sr=sr)
  fingerprint = np.mean(mfccs.T, axis=0)
  fingerprint_bytes = fingerprint.tobytes()

  cur.execute("SELECT * FROM songs")
  songs = cur.fetchall()

  best_match = None
  best_distance = float("inf")
  for song_name, db_fingerprint in songs:
    distance = np.linalg.norm(np.frombuffer(db_fingerprint, dtype=np.float32) - fingerprint)
    if distance < best_distance:
      best_match = song_name
      best_distance = distance

  similarity = 1 / (1 + best_distance) * 100

  if best_match:
    logger.info(f"Most similar song: {best_match} (Similarity: {similarity:.2f}%)")
  else:
    logger.info("No matching songs found in database.")

  return best_match, similarity
    
        
async def identify_music(file, platform_name="Radio King"):
    # Generat eunique name
    unique_name = str(int(time.time()))
    file_path = f"{os.path.join(UPLOAD_DIR, unique_name)}.mp3"
    with open(f"{file_path}", "wb") as buffer:
        buffer.write(file.file.read())
    
    best_match, similarity = identify_song(file_path)
    music = music_collection.find_one({"_id": ObjectId(best_match)})
    if similarity < 50:
        print(music)
        if music:
            platform_records = music['platform_details']
            for platform in platform_records:
                if platform['platform_name'] == platform_name:
                    platform['stream_count'] = str(int(platform['stream_count']) + 1)
                    platform['records'].append({
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'time': datetime.datetime.now().strftime("%H:%M:%S"),
                        'count': int(platform['stream_count'])+1,
                        'duration': "0"
                    })
                    music_collection.update_one({"_id": ObjectId(best_match)}, {"$set": {"platform_details": platform_records}})
                    
                    music_outer = music_collection.find_one({"_id": ObjectId(best_match)})
                    music_outer['total_stream'] = str(int(music_outer['total_stream']) + 1)
                    music_collection.update_one({"_id": ObjectId(best_match)}, {"$set": music_outer})
                    break
            
        return MusicTrainResponse(
            code=200,
            response="Music Identified",
            data=MusicNew(id=best_match)
        )
    else:
        return MusicTrainResponse(
            code=404,
            response="Music Not Identified",
            data=None
        )
    
    #     logger.info("Tryint the API")
    #     result = support.find_musics_in_the_audio(file_path)
    #     logger.info(f"Song Idenfied to: {result}")
        
    #     music_details = {
    #         'date': datetime.datetime.now().strftime("%Y-%m-%d"),
    #         'time': datetime.datetime.now().strftime("%H:%M:%S"),
    #         "title": result["result"][0]["title"],
    #         'platform': 'Radioking Stream',
    #         'count': 1,
    #         'duration': "0"
    #     }
        
        
async def get_music_data(music) -> MusicResponseModel:
    
    music_details = music_collection.find()
    musics = []
    
    for music_de in music_details:
        if music_de['user_id'] == music:
            musics.append(MusicResponse(id=str(music_de["_id"]), **music_de))
    
    if music_details:
        return MusicResponseModel(
            code=200,
            response="Music Data Retrieved",
            data=musics
        )
    else:
        return MusicResponseModel(
            code=404,
            response="Music Data Not Retrieved",
            data=None
        )