import numpy as np
from app.utils import config
from app.api.music_identifier.libraries.libs.find_match import find_matches
from app.api.music_identifier.libraries.libs.db import get_conn
import os
from pydub import AudioSegment
from app.utils.logging import get_logger

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
        return None, None

    audio = AudioSegment.from_file(audio_file)
    temp_folder = "/app/temp/temp.wav"
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
        for item in matches:
            title = str(item[0])
            if title in identified_songs.keys():
                identified_songs[title] += 1
            else:
                identified_songs[title] = 1

        song_id = max(identified_songs, key=identified_songs.get)
        conn, cur = get_conn()

        cur.execute("SELECT title FROM songs WHERE id=%s", song_id)

        song_details = cur.fetchall()

        prob = (identified_songs[song_id] / len(matches)) * 100

        logger.info(f"Total Identified songs = {len(identified_songs)}")
        title= song_details[0][0]
        propability = prob
        logger.info(f"Best hit -> Title: {title} with {propability}% confidence")
        
        return title, propability

    os.remove(temp_folder)