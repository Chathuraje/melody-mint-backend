from fastapi import APIRouter
from app.api.music_identifier.routes.music_identifier import router as music_identifier_routers

router = APIRouter(
    tags=["Music Identifier"],
    prefix="/audio"
)

router.include_router(music_identifier_routers)
