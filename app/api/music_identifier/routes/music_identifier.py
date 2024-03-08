from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.logging import get_logger
from app.api.music_identifier.libraries import music_identifier
from app.utils.response import MusicTrainResponse
from app.models.MusicIdentifier import Music



router = APIRouter()
logger = get_logger()


@router.post("/train", response_model=MusicTrainResponse)
async def identify_uploaded_music(music: Music, file: UploadFile = File(...)):
    logger.info("Training music")
    return await music_identifier.train_music(music, file)

@router.post("/identify", response_model=MusicTrainResponse)
async def identify_uploaded_music(music: Music, file: UploadFile = File(...)):
    logger.info("Identifying music")
    return await music_identifier.identify_music(music, file)

@router.get("/get_data", response_model=MusicTrainResponse)
async def get_music_data(music: Music):
    logger.info("Getting music data")
    return await music_identifier.get_music_data(music)