from fastapi import APIRouter, HTTPException
from app.utils.logging import get_logger
from app.api.marketplace.libraries import marketplace
from app.utils.response import CollectionCreateResponse, AllCollectionResponse, SingleCollectionResponse, NFTCreateResponse, AllNFTResponse, SingleNFTResponse
from app.models.Marketplace import Collections, NFT, CollectionNew


router = APIRouter()
logger = get_logger()

@router.get("/", response_model=AllCollectionResponse)
async def get_all_collections():
    logger.info("Getting all Collections")
    return await marketplace.get_all_collections()

# @router.post("/create_collection", response_model=CollectionCreateResponse)
# async def create_collection(collections: Collections):
#     logger.info("Creating a new collection")
#     return await marketplace.create_collection(collections)

@router.get("/{collection_id}", response_model=SingleCollectionResponse)
async def get_collection(collection_id: str):
    logger.info(f"Getting collection details with ID: {collection_id}")
    return await marketplace.get_campaign(collection_id)

@router.put("/{collection_id}", response_model=SingleCollectionResponse)
async def update_collection(collection_id: str, collections: Collections):
    logger.info(f"Updating collection with ID: {collection_id}")
    return await marketplace.update_collection(collection_id, collections)

@router.get("/{collection_id}/nfts", response_model=AllNFTResponse)
async def get_nfts(collection_id: str):
    logger.info(f"Getting NFTs for collection with ID: {collection_id}")
    return await marketplace.get_nfts(collection_id)

@router.post("/{collection_id}/nfts/create_nft", response_model=NFTCreateResponse)
async def create_nft(collection_id: str, nft: NFT):
    logger.info(f"Creating a new NFT for collection with ID: {collection_id}")
    return await marketplace.create_nft(collection_id, nft)

@router.get("/{collection_id}/nfts/{nft_id}", response_model=SingleNFTResponse)
async def get_nft(collection_id: str, nft_id: str):
    logger.info(f"Getting NFT with ID: {nft_id} for collection with ID: {collection_id}")
    return await marketplace.get_nft(collection_id, nft_id)

@router.put("/{collection_id}/nfts/{nft_id}", response_model=SingleNFTResponse)
async def update_nft(collection_id: str, nft_id: str, nft: NFT):
    logger.info(f"Updating NFT with ID: {nft_id} for collection with ID: {collection_id}")
    return await marketplace.update_nft(collection_id, nft_id, nft)

@router.put("/{collection_id}/nfts/{nft_id}/transfer", response_model=SingleNFTResponse)
async def transfer_nft(collection_id: str, nft_id: str, owner_id: str):
    logger.info(f"Transferring NFT with ID: {nft_id} for collection with ID: {collection_id}")
    return await marketplace.transfer_nft(collection_id, nft_id, owner_id)