import numpy as np
from app.utils import config
from app.api.music_identifier.libraries.libs.find_match import find_matches
from app.api.music_identifier.libraries.libs.db import get_conn
import os
from pydub import AudioSegment
from app.utils.logging import get_logger
from bson import ObjectId

from app.utils.database import music_collection


logger = get_logger()  

def identify_from_file(audio_file):
    """Identifies audio from a file.

    Identifies the song from an audio file and works with local file paths.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        None
    """

    if not os.path.exists(audio_file):
        logger.info("Audio file not found")
        return None

    audio = AudioSegment.from_file(audio_file)
    temp_folder = "app/temp/temp.wav"
    audio.export(temp_folder, format="wav")  # Convert to WAV format
    frames = [open(temp_folder, "rb").read()]

    data = [[] for _ in range(config.DEFAULT_CHANNELS)]
    for item in frames:
        nums = np.frombuffer(item, np.int16)
        for c in range(config.DEFAULT_CHANNELS):
            data[c].extend(nums[c::config.DEFAULT_CHANNELS])

    matches = []
    logger.info("Finding Song...")
    for channeln, channel in enumerate(data):
        logger.info(f"Processing channel {channeln + 1}/2")
        matches.extend(find_matches(channel))

    identified_songs = {}
    if len(matches) > 0:
        for song_id  in matches:
            if song_id in identified_songs.keys():
                identified_songs[song_id] += 1
            else:
                identified_songs[song_id] = 1

    if identified_songs:
        song_id = max(identified_songs, key=identified_songs.get)
        conn, cur = get_conn()
        
        musics = music_collection.find_one({"_id": ObjectId(song_id)})
        
        if musics:
            prob = (identified_songs[song_id] / len(matches)) * 100
            logger.info(f"Probability of song: {prob}%")
            if prob > 25:
                logger.info(f"Total Identified songs = {len(identified_songs)}")
                title= musics["title"]
                song_hash = musics["hash"]
                propability = prob
                logger.info(f"Best hit -> Title: {title} with {propability}% confidence")
                
                return title, propability, song_hash
            else:
                logger.info("No Song Found")
                return None
        else:
            logger.info("No Song Found")
            return None
    else:
        logger.info("No Song Found")
        return None

    os.remove(temp_folder)