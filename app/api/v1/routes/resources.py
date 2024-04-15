from fastapi import APIRouter, status
from app.utils import logging
from app.api.v1.libraries.resouerces import resouerces

resources_router = APIRouter(
    prefix="/res", tags=["Resouerces"], responses={404: {"description": "Not found"}}
)
logger = logging.getLogger()


@resources_router.get(
    "/images",
    description="Get Images",
    status_code=status.HTTP_200_OK,
)
async def get_images(image_name: str):
    logger.info("Get Images endpoint accessed")
    return await resouerces.get_images(image_name)
