from app.utils.response import MusicTrainResponse

async def train_music(music, file):
    contents = await file.read()
    
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