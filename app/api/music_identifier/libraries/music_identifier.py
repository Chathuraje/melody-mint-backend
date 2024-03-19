from app.utils.response import MusicTrainResponse, MusicResponseModel
import datetime
import time
import os
# from app.api.music_identifier.libraries import support
from app.utils.database import music_collection, user_collection
from app.models.MusicIdentifier import MusicNew, MusicResponse
from bson import ObjectId
from app.api.music_identifier.libraries import identify
from app.api.music_identifier.libraries import train
import hashlib
# from app.api.music_identifier.libraries import assemblyai
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from app.utils.logging import get_logger
logger = get_logger()  
<<<<<<< HEAD
=======
    
UPLOAD_DIR = "app/temp/songs/"
>>>>>>> development

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_text = [word for word in word_tokens if word.isalnum() and word not in stop_words]
    return set(filtered_text)

def calculate_normalized_similarity(original_text, new_text):
    original_set = preprocess_text(' '.join(original_text))
    new_set = preprocess_text(' '.join(new_text))
    intersection = len(original_set.intersection(new_set))
    union = len(original_set.union(new_set))
    similarity = intersection / union if union != 0 else 0
    # Normalize the similarity score
    normalized_similarity = (similarity / len(original_text)) * 100
    return normalized_similarity

def calculate_song_hash(file_path):
    logger.info("Calculating Single hash for Song")
    with open(file_path, "rb") as f:
        song_data = f.read()
        song_hash = hashlib.sha256(song_data).hexdigest()
        logger.info(f"Hash for song: {song_hash}")
        
        return song_hash
    
    
async def train_music(file, song_name, user_id):
<<<<<<< HEAD
    DB_FILE = "app/data/music.db"
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()    
    UPLOAD_DIR = "app/temp/songs/"
    create_table()
=======
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        return MusicTrainResponse(
            code=404,
            response="User Not Found",
            data=None
        )
    
>>>>>>> development
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generat eunique name
    unique_name = str(int(time.time()))
    file_path = f"{os.path.join(UPLOAD_DIR, unique_name)}.mp3"
    with open(f"{file_path}", "wb") as buffer:
        buffer.write(file.file.read())
        
    song_hash = calculate_song_hash(file_path)
    music = music_collection.find_one({"hash": song_hash})
    
    if music is None:
        status = train.create_finger_prints(file_path, song_hash, song_name)
        music_details = {}
        
        if status:
            # transcript = assemblyai.generate_transcript(file_path)
            # if transcript is not None:
            #     music_details['transcript'] = transcript
                    
            platform_name = "Radio King"
            music_details['title'] = str(song_name)
            music_details['user_id'] = str(user_id)
            music_details['type'] = 'music'
            music_details['total_stream'] = "0"
            music_details['total_platform'] = "1"
            music_details['total_time'] = "0"
            music_details['hash'] = song_hash
            
            
            platform_records = [
                {
                    'platform_name': platform_name,
                    'stream_count': "0",
                    'records': []
                }
            ]
            music_details['platform_details'] = platform_records
            
            musics = music_collection.insert_one(music_details)
            return MusicTrainResponse(
                code=200,
                response="Music Trained",
                data=MusicNew(id=str(musics.inserted_id))
            )
        else:
            return MusicTrainResponse(
                code=404,
                response="Music Already Trained or Error Occured",
                data=None
            )
    else:
        logger.info("Music Already Trained")
        return MusicTrainResponse(
            code=409,
            response="Music Already Trained",
            data=None
        )


async def identify_music(file, platform_name="Radio King"):
    # Generat eunique name
    unique_name = str(int(time.time()))
    file_path = f"{os.path.join(UPLOAD_DIR, unique_name)}.mp3"
    with open(f"{file_path}", "wb") as buffer:
        buffer.write(file.file.read())
    
    song_identification = identify.identify_from_file(file_path)
    if song_identification is None:
        return MusicTrainResponse(
            code=404,
            response="Music Not Identified",
            data=MusicNew(id=None)
        )
    else:
        title, similarity, song_hash = song_identification
        music = music_collection.find_one({"hash": song_hash})
        if similarity > 25:
            if music:
                original_transcript = music['transcript']
                # new_transcript = assemblyai.generate_transcript(file_path)
                # if new_transcript is not None:
                    # similarity = calculate_normalized_similarity(original_transcript, new_transcript)
                if True:
                    logger.info(f"Transcript Similarity:  {similarity}")
                    if similarity > 25:
                        song_id = music['_id'] 
                        platform_records = music['platform_details']
                        for platform in platform_records:
                            if platform['platform_name'] == platform_name:
                                platform['stream_count'] = str(int(platform['stream_count']) + 1)
                                platform['records'].append({
                                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                                    'time': datetime.datetime.now().strftime("%H:%M:%S"),
                                    'duration': "0"
                                })
                                music_collection.update_one({"_id": ObjectId(song_id)}, {"$set": {"platform_details": platform_records}})
                                
                                music_outer = music_collection.find_one({"_id": ObjectId(song_id)})
                                music_outer['total_stream'] = str(int(music_outer['total_stream']) + 1)
                                music_collection.update_one({"_id": ObjectId(song_id)}, {"$set": music_outer})
                                logger.info(f"100% Music Identifed: {title}")
                                return MusicTrainResponse(
                                    code=200,
                                    response="Music Identified",
                                    data=MusicNew(id=str(song_id))
                                )
                            else:
                                logger.info("Platform Not Found")
                    else:
                        logger.info("Transcript Not Matched, Music Not Identified")
                        return MusicTrainResponse(
                            code=404,
                            response="Music Not Identified",
                            data=None
                        )
                else:
                    logger.info("Transcript Not Found, Music Not Identified")
                    return MusicTrainResponse(
                        code=404,
                        response="Music Not Identified",
                        data=None
                    )
            else:
                logger.info("Music Not Found")
                return MusicTrainResponse(
                    code=404,
                    response="Music Not Found",
                    data=None
                )
        else:
            logger.info("Music Not Found")
            return MusicTrainResponse(
                code=404,
                response="Music Not Found",
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