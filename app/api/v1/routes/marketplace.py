from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.api.v1.responses.marketplace import (
    MarketplaceResponse,
    NFTResponse,
    SinglNFTResponseWithMarketplace,
)
from app.api.v1.responses.user import UserResponse
from app.utils import logging
from app.api.v1.libraries.user import user
from app.api.v1.libraries.marketplace import marketplace


marketplace_router = APIRouter(
    prefix="/marketplace",
    tags=["Marketplace"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger()


user_dependency = Annotated[UserResponse, Depends(user.get_profile)]


@marketplace_router.get(
    "/{chain_id}",
    description="Get marketplace",
    response_model=list[MarketplaceResponse],
    status_code=status.HTTP_200_OK,
)
async def get_marketplace(chain_id: int):
    logger.info("Get Marketplace endpoint accessed.")
    return await marketplace.get_marketplace(chain_id)


@marketplace_router.get(
    "/nfts/{chaind_id}/{collection_address}",
    description="Get NFTs",
    response_model=NFTResponse,
)
async def get_nfts(chaind_id: int, collection_address: str):
    logger.info("Get NFTs endpoint accessed.")
    return await marketplace.get_nfts(chaind_id, collection_address)


@marketplace_router.get(
    "/nft/{chaind_id}/{collection_address}/{nft_id}",
    description="Get NFT",
    response_model=SinglNFTResponseWithMarketplace,
)
async def get_single_nft(chaind_id: int, collection_address: str, nft_id: str):
    logger.info("Get NFTs endpoint accessed.")
    return await marketplace.get_single_nft(chaind_id, collection_address, nft_id)
