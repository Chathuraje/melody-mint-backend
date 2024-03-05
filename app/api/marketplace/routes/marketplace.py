from fastapi import APIRouter, HTTPException
from app.utils.logging import get_logger
from app.api.campaigns.libraries import campaigns


router = APIRouter()
logger = get_logger()

@router.get("/")
async def get_all_campaigns():
    logger.info("Getting all users")
    return await campaigns.get_all_campaigns()