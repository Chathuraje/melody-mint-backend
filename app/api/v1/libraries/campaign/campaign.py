import json
from fastapi import UploadFile
from app.api.v1.libraries.campaign.ipfs import pinFiletoIPFS, pinFiletoJSON
from app.api.v1.model.Campaign import CampaignOffChain, CollectionOffChain
from app.api.v1.responses.campaign import CampaignCreateResponse
from config import settings

env = settings.get_settings()


async def create_campaign(
    campaign_data: CampaignOffChain,
    collection_data: CollectionOffChain,
    collection_image: UploadFile,
    collection_hero: UploadFile,
    image: UploadFile,
) -> CampaignCreateResponse:

    PINATA_IPFS_URI = env.PINATA_IPFS_URI

    ipfs_collection_image = await pinFiletoIPFS(collection_image)
    if ipfs_collection_image is None:
        raise Exception("Failed to pin creation image to IPFS")

    ipfs_collection_hero = await pinFiletoIPFS(collection_hero)
    if ipfs_collection_hero is None:
        raise Exception("Failed to pin creation hero to IPFS")

    ipfs_image = await pinFiletoIPFS(image)
    if ipfs_image is None:
        raise Exception("Failed to pin image to IPFS")

    json_data_campaign = {
        "description": campaign_data.description,
        "short_description": campaign_data.short_description,
        "image": f"{PINATA_IPFS_URI}/{ipfs_image}",
    }
    ipfs_json_data_campaign = await pinFiletoJSON(json_data_campaign)

    json_data_collection = {
        "collection_description": collection_data.collection_description,
        "collection_image": f"{PINATA_IPFS_URI}/{ipfs_collection_image}",
        "collection_hero": f"{PINATA_IPFS_URI}/{ipfs_collection_hero}",
    }
    ipfs_json_data_campaign = await pinFiletoJSON(json_data_collection)

    return CampaignCreateResponse(
        campaign_data=ipfs_json_data_campaign, collection_data=ipfs_json_data_campaign
    )
