from fastapi import APIRouter, UploadFile, File
from app.utils.logging import get_logger
from app.api.video_identifier.libraries import video_identifier
from app.utils.response import VideoTrainResponse
from app.models.VideoIdentifier import Video



router = APIRouter()
logger = get_logger()


@router.post("/train", response_model=VideoTrainResponse)
async def train_video(video: Video, file: UploadFile = File(...)):
    logger.info("Training video")
    return await video_identifier.train_video(video, file)

@router.post("/identify", response_model=VideoTrainResponse)
async def identify_uploaded_video(video: Video, file: UploadFile = File(...)):
    logger.info("Identifying video")
    return await video_identifier.identify_video(video, file)

@router.get("/get_data", response_model=VideoTrainResponse)
async def get_video_data(video: Video):
    logger.info("Getting video data")
    return await video_identifier.get_video_data(video)