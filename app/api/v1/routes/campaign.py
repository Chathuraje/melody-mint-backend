from itertools import chain
import json
from time import sleep
from typing import Annotated
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from app.api.v1.model.Campaign import CampaignOffChain, CollectionOffChain
from app.api.v1.responses.campaign import (
    CampaignCreateResponse,
    CampaignsResponse,
)
from app.api.v1.responses.user import UserResponse
from app.utils import logging
from app.api.v1.libraries.user import user
from app.api.v1.libraries.campaign import campaign

campaing_router = APIRouter(
    prefix="/campaign", tags=["Campaign"], responses={404: {"description": "Not found"}}
)
logger = logging.getLogger()


user_dependency = Annotated[UserResponse, Depends(user.get_profile)]


@campaing_router.get(
    "/{chain_id}",
    description="Get Campaign",
    response_model=list[CampaignsResponse],
    status_code=status.HTTP_200_OK,
)
async def get_campaigns(chain_id: int):
    logger.info("Get Campaign endpoint accessed.")
    return await campaign.get_campaigns(chain_id)


@campaing_router.get(
    "/{chain_id}/{campaign_id}",
    description="Get Campaign by ID",
    response_model=CampaignsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_campaign_by_id(chain_id: int, campaign_id: int):
    logger.info("Get Campaign by ID endpoint accessed.")
    return await campaign.get_campaign_by_id(chain_id, campaign_id)


@campaing_router.post(
    "/",
    description="Create Fundraiser Campaign",
    response_model=CampaignCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def create_campaign(
    access_user: user_dependency,
    campaign_data=Form(None),
    collection_data=Form(None),
    collection_image: UploadFile = File(None),
    collection_hero: UploadFile = File(None),
    image: UploadFile = File(None),
):
    logger.info("Create Campaign endpoint accessed.")
    campaign_data = json.loads(campaign_data)
    campaign_data.pop("image", None)

    collection_data = json.loads(collection_data)
    collection_data.pop("collection_image", None)
    collection_data.pop("collection_hero", None)

    campaign_data = CampaignOffChain(**campaign_data)
    collection_data = CollectionOffChain(**collection_data)

    return await campaign.create_campaign(
        campaign_data, collection_data, collection_image, collection_hero, image
    )
