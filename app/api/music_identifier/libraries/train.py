import os
import eyed3
from app.api.music_identifier.libraries.libs.parse_audio import parse_bytes
from app.api.music_identifier.libraries.libs.generate_fingerprint import fingerprint
from app.api.music_identifier.libraries.libs.db import get_conn
from app.utils.logging import get_logger
from app.api.music_identifier.libraries import identify
from app.utils.database import music_collection, song_fingerprints

logger = get_logger()  

def get_tags(file):
    audio = eyed3.load(file)
    tags = audio.tag
    song_name = None
    artist = None
    album = None
    
    if tags is None:
        title = file.split('/')
        song_name = title[len(title) - 1]
        song = [song_name, 'unknown', 'unknown']
    else:
        if tags.title is None:
            title = file.split('/')
            song_name, _ = os.path.splitext(title[len(title) - 1])
        else:
            song_name = tags.title
            artist = tags.artist
            album = tags.album
            
            if artist is None:
                artist = 'Unknown'

            if album is None:
                album = 'Unknown'

        song = [song_name, artist, album]

    return song


def create_finger_prints(mp3_file_path, musics_id):
    
    musics = music_collection.find_one({"_id": musics_id})
    
    song = parse_bytes(mp3_file_path, offline=True)
    logger.info(f"Fingerprinting song: {musics['title']}")
    hashes = set()
    channel_amount = len(song['channels'])
    for channel_number, channel in enumerate(song['channels']):
        channel_hashes = fingerprint(channel, sampling_rate=song['frame_rate'])
        channel_hashes = set(channel_hashes)

        logger.info(f"finished channel {channel_number + 1}/{channel_amount}, got {len(channel_hashes)} hashes")

        hashes |= channel_hashes

    values = []
    for h, offset in hashes:
        values.append({"song_id": str(musics_id), "hash": h, "offset": int(offset)})
        
    logger.info(f"Got {len(values)} hashes for {musics['title']}")
    if len(values) > 0:
        logger.info("Done")
        song_fingerprints.insert_many(values)
            
        return musics_id
    else:
        return None
    
