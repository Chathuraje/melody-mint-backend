from fastapi import APIRouter, HTTPException
from app.utils.logging import get_logger
from app.api.campaigns.libraries import campaigns
from app.utils.response import CampaignCreateResponse, SingleCampaignResponse, AllCampaignResponse, InvestmentResponse
from app.models.Campaigns import Campaigns, InvestCampaign


router = APIRouter()
logger = get_logger()

@router.get("/", response_model=AllCampaignResponse)
async def get_all_campaigns():
    logger.info("Getting all users")
    return await campaigns.get_all_campaigns()

@router.get("/users/{user_id}", response_model=AllCampaignResponse)
async def get_user_campaigns(user_id: str):
    logger.info(f"Getting all campaigns for user with ID: {user_id}")
    return await campaigns.get_user_campaigns(user_id)


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
async def update_campaign(campaign_id: str, campaign: Campaigns):
    logger.info(f"Updating campaign with ID: {campaign_id}")
    updated_campaign = await campaigns.update_campaign(campaign_id, campaign)
    if updated_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return updated_campaign

@router.put("/{campaign_id}/invest", response_model=InvestmentResponse)
async def invest_campaign(campaign_id: str, investment_details: InvestCampaign):
    logger.info(f"Investing in campaign with ID: {campaign_id}")
    updated_campaign = await campaigns.invest_campaign(campaign_id, investment_details)
    if updated_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return updated_campaign

@router.get('/get_investments/{user_id}', response_model=AllCampaignResponse)
async def get_investments(user_id: str):
    logger.info(f"Getting investments for user with ID: {user_id}")
    return await campaigns.get_investments(user_id)