from app.utils.response import VideoTrainResponse

async def train_video(video, file):
    contents = await file.read()
    
    # store data in database
    
    
    # Training Steps
    video_details = {}
    if video_details:
        return VideoTrainResponse(
            code=200,
            response="video Trained",
            data=video_details
        )
    else:
        return VideoTrainResponse(
            code=404,
            response="video is Not Trained",
            data=None
        )
        
async def identify_video(video, file):
    contents = await file.read()
    
    # Identification Steps
    video_details = {}
    if video_details:
        return VideoTrainResponse(
            code=200,
            response="video Identified",
            data=video_details
        )
    else:
        return VideoTrainResponse(
            code=404,
            response="video is Not Identified",
            data=None
        )
        
        
async def get_video_data(video):
    # Get video Data
    video_details = {}
    if video_details:
        return VideoTrainResponse(
            code=200,
            response="video Data Retrieved",
            data=video_details
        )
    else:
        return VideoTrainResponse(
            code=404,
            response="video Data Not Retrieved",
            data=None
        )