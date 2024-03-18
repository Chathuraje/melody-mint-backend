from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.utils.logging import get_logger
from app.api.music_identifier.libraries import music_identifier
from app.utils.response import MusicTrainResponse, MusicIdentifierResponse, MusicResponseModel
from app.models.MusicIdentifier import MusicResponse



router = APIRouter()
logger = get_logger()

@router.get("/{user_id}", response_model=MusicResponseModel)
async def get_music_data(user_id: str):
    logger.info("Getting music data")
    return await music_identifier.get_music_data(user_id)

@router.post("/train", response_model=MusicTrainResponse)
async def train_music(file: UploadFile = File(...), song_name: str = Form(...), user_id: str = Form(...)):
    try:
        logger.info("Training music")
        return await music_identifier.train_music(file, song_name, user_id)
    except Exception as e:
        logger.error(f"Error training music: {e}")
        raise HTTPException(status_code=500, detail="Error training music")

@router.post("/identify", response_model=MusicIdentifierResponse)
async def identify_uploaded_music(file: UploadFile = File(...)):
    logger.info("Identifying music")
    return await music_identifier.identify_music(file)