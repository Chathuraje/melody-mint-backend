from app.utils.response import MusicTrainResponse

async def train_music(music, file):
    contents = await file.read()
    
    # store data in database
    
    
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