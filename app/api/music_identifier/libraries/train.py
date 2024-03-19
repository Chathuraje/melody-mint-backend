import os
import eyed3
from app.api.music_identifier.libraries.libs.parse_audio import parse_bytes
from app.api.music_identifier.libraries.libs.generate_fingerprint import fingerprint
from app.api.music_identifier.libraries.libs.db import get_conn
from app.utils.logging import get_logger
from app.api.music_identifier.libraries import identify

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


def create_finger_prints(mp3_file_path, song_hash, song_name):

    conn, cur = get_conn()
    song = parse_bytes(mp3_file_path, offline=True)
    check = cur.execute("SELECT id FROM songs WHERE hash=%s", song_hash)
    if check > 0:
        logger.info("Skipping File... Fingerprint already available...")
        return False
    else:
        cur.execute("INSERT INTO songs(title, hash) VALUES(%s, %s)", [song_name, song_hash])
        conn.commit()
        logger.info(f"Fingerprinting song: {song_name}")
        hashes = set()
        channel_amount = len(song['channels'])
        for channel_number, channel in enumerate(song['channels']):
            channel_hashes = fingerprint(channel, sampling_rate=song['frame_rate'])
            channel_hashes = set(channel_hashes)

            logger.info(f"finished channel {channel_number + 1}/{channel_amount}, got {len(channel_hashes)} hashes")

            hashes |= channel_hashes

        values = []
        check = cur.execute("SELECT id FROM songs WHERE hash=%s", song_hash)
        rows = cur.fetchall()
        for h, offset in hashes:
            values.append((rows[0][0], h, int(offset)))

        logger.info(f"Got {len(values)} hashes for {song_name}")
        if len(values) > 0:
            logger.info("Done")
            cur.executemany(
                "INSERT INTO fingerprints(song_id, hash, offset) VALUES(%s,%s,%s)",
                values
            )
            conn.commit()
            return True
            

    cur.close()
    return False
    
