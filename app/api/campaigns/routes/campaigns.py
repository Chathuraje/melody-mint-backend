from fastapi import APIRouter, HTTPException
from app.utils.logging import get_logger
from app.api.campaigns.libraries import campaigns
from app.utils.response import CampaignCreateResponse, SingleCampaignResponse, AllCampaignResponse
from app.models.Campaigns import Campaigns


router = APIRouter()
logger = get_logger()

@router.get("/", response_model=AllCampaignResponse)
async def get_all_campaigns():
    logger.info("Getting all users")
    return await campaigns.get_all_campaigns()

@router.post("/create_campaign", response_model=CampaignCreateResponse)
async def create_campaign(campaign: Campaigns):
    logger.info("Creating a new campaign")
    return await campaigns.create_campaign(campaign)

@router.get("/{campaign_id}", response_model=SingleCampaignResponse)
async def get_campaign(campaign_id: str):
    logger.info(f"Getting campaign details with ID: {campaign_id}")
    user = await campaigns.get_campaign(campaign_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{campaign_id}", response_model=SingleCampaignResponse)
async def update_campaign(campaign_id: str, user: Campaigns):
    logger.info(f"Updating campaigns details with ID: {campaign_id}")
    updated_user = await campaigns.update_campaign(campaign_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
