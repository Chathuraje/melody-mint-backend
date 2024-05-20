from typing import Annotated
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from app.api.v1.model.MusicIdentifier import Music, MusicNew
from app.api.v1.responses.music_identifier import MusicResponse
from app.api.v1.responses.user import UserResponse
from app.utils import logging
from app.api.v1.libraries.music_identifier import music_identifier
from app.api.v1.libraries.user import user

logger = logging.getLogger()

music_identifier_router = APIRouter(
    prefix="/music_identifier", tags=["Music Identifier"]
)

user_dependency = Annotated[UserResponse, Depends(user.get_profile)]


@music_identifier_router.get("/", response_model=list[MusicResponse])
async def get_music_data(
    user_data: user_dependency,
):
    logger.info("Getting music data")
    return await music_identifier.get_music_data(user_data.id)


@music_identifier_router.post("/train", response_model=MusicNew)
async def train_music(
    user_data: UserResponse, file: UploadFile = File(...), song_name: str = Form(...)
):
    try:
        logger.info("Training music")
        return await music_identifier.train_music(file, song_name, user_data.id)
    except Exception as e:
        logger.error(f"Error training music: {e}")
        raise HTTPException(status_code=500, detail="Error training music")


@music_identifier_router.post("/identify", response_model=Music)
async def identify_uploaded_music(file: UploadFile = File(...)):
    logger.info("Identifying music")
    return await music_identifier.identify_music(file)
