import datetime
import time
import os
from bson import ObjectId
import hashlib
from app.api.v1.libraries.music_identifier.libraries.identify import identify_from_file
from app.api.v1.libraries.music_identifier.libraries.train import create_finger_prints
from app.api.v1.model.MusicIdentifier import MusicNew
from app.api.v1.responses.music_identifier import MusicResponse
from app.utils import logging
from config.database import get_collection

logger = logging.getLogger()

UPLOAD_DIR = "app/api/v1/upload/temp"


def calculate_song_hash(file_path):
    logger.info("Calculating Single hash for Song")
    with open(file_path, "rb") as f:
        song_data = f.read()
        song_hash = hashlib.sha256(song_data).hexdigest()
        logger.info(f"Hash for song: {song_hash}")

        return song_hash


async def train_music(file, song_name, user_id):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generat eunique name
    unique_name = str(int(time.time()))
    file_path = f"{os.path.join(UPLOAD_DIR, unique_name)}.mp3"
    with open(f"{file_path}", "wb") as buffer:
        buffer.write(file.file.read())

    song_hash = calculate_song_hash(file_path)
    music_details = {
        "title": str(song_name),
        "user_id": str(user_id),
        "type": "music",
        "total_stream": "0",
        "total_platform": "1",
        "total_time": "0",
        "hash": song_hash,
        "platform_details": [
            {"platform_name": "Radio King", "stream_count": "0", "records": []}
        ],
    }

    music_collection = await get_collection("musics")
    musics = await music_collection.find_one({"hash": song_hash})
    if musics:
        musics_id = musics["_id"]
    else:
        musics = await music_collection.insert_one(music_details)
        musics_id = musics.inserted_id

    song_fingerprints = await get_collection("song_fingerprints")
    count = await song_fingerprints.count_documents({"song_id": musics_id})
    logger.info(f"Sum of the count: {count}")

    if count == 0:
        logger.info("No Fingerprints Found. Start Training Process")
        music_id = await create_finger_prints(file_path, musics_id)

        if music_id:
            return MusicNew(id=str(music_id))
        else:
            return MusicNew(id=None)
    else:
        logger.info("Music Already Trained")
        return MusicNew(id=str(musics_id))


async def identify_music(file, platform_name="Radio King"):
    # Generat eunique name
    unique_name = str(int(time.time()))
    file_path = f"{os.path.join(UPLOAD_DIR, unique_name)}.mp3"
    with open(f"{file_path}", "wb") as buffer:
        buffer.write(file.file.read())

    song_identification = await identify_from_file(file_path)
    if song_identification is None:
        return MusicNew(id=None)
    else:
        title, similarity, song_hash = song_identification
        if similarity > 25:

            music_collection = await get_collection("musics")
            music = await music_collection.find_one({"hash": song_hash})
            if music:
                song_id = music["_id"]
                platform_records = music["platform_details"]
                for platform in platform_records:
                    if platform["platform_name"] == platform_name:
                        platform["stream_count"] = str(
                            int(platform["stream_count"]) + 1
                        )
                        platform["records"].append(
                            {
                                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                                "duration": "0",
                            }
                        )
                        await music_collection.update_one(
                            {"_id": ObjectId(song_id)},
                            {"$set": {"platform_details": platform_records}},
                        )

                        music_outer = await music_collection.find_one(
                            {"_id": ObjectId(song_id)}
                        )
                        if music_outer is not None:
                            music_outer["total_stream"] = str(
                                int(music_outer["total_stream"]) + 1
                            )
                            await music_collection.update_one(
                                {"_id": ObjectId(song_id)}, {"$set": music_outer}
                            )
                            logger.info(f"100% Music Identifed: {title}")
                            return MusicNew(id=str(song_id))
                        else:
                            logger.info("Music Not Found")
                            return MusicNew(id=None)
                    else:
                        logger.info("Platform Not Found")
            else:
                logger.info("Music Not Found")
                return MusicNew(id=None)
        else:
            logger.info("Music Not Found")
            return MusicNew(id=None)

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


async def get_music_data(music) -> list[MusicResponse] | None:
    try:
        music_collection = await get_collection("musics")
        music_details = await music_collection.find().to_list(length=None)

        musics = []

        for music_de in music_details:
            if music_de["user_id"] == music:
                musics.append(MusicResponse(id=str(music_de["_id"]), **music_de))
                
        if music_details:
            return musics
        else:
            return None

    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
