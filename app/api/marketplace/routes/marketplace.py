from fastapi import APIRouter, HTTPException
from app.utils.logging import get_logger
from app.api.marketplace.libraries import marketplace
from app.utils.response import CollectionCreateResponse, AllCampaignResponse, SingleCampaignResponse
from app.models.Marketplace import Collections, NFT, CollectionNew


router = APIRouter()
logger = get_logger()

@router.get("/", response_model=AllCampaignResponse)
async def get_all_collections():
    logger.info("Getting all Collections")
    return await marketplace.get_all_collections()

@router.post("/create_collection", response_model=CollectionCreateResponse)
async def create_collection(collections: Collections):
    logger.info("Creating a new collection")
    return await marketplace.create_collection(collections)

@router.get("/{collection_id}", response_model=SingleCampaignResponse)
async def get_collection(collection_id: str):
    logger.info(f"Getting collection details with ID: {collection_id}")
    return await marketplace.get_campaign(collection_id)