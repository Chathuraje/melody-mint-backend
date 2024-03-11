from fastapi import APIRouter
from app.api.video_identifier.routes.video_identifier import router as video_identifier_routers

router = APIRouter(
    tags=["Video Identifier"],
    prefix="/video"
)

router.include_router(video_identifier_routers)
