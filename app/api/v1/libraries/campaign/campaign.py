import json
from fastapi import UploadFile
from app.utils.ipfs import pinFiletoIPFS, pinFiletoJSON, readFromIPFS
from app.api.v1.model.Campaign import CampaignOffChain, CollectionOffChain
from app.api.v1.responses.campaign import (
    CampaignCreateResponse,
    CampaignsResponse,
)
from config import settings
from config.web3 import web3_get_contract

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


async def get_campaigns(chain_id: int) -> list[CampaignsResponse]:
    contract = await web3_get_contract(chain_id)
    result = contract.functions.getAllCampaigns().call()

    campaigns = []
    for campaign_data in result:
        campaign_meta_data = campaign_data[8]
        data = await readFromIPFS(campaign_meta_data)
        if data is None:
            raise Exception("Failed to read from IPFS")

        collection_description = data["collection_description"]
        collection_image = data["collection_image"]
        collection_hero = data["collection_hero"]

        campaign = CampaignsResponse(
            fundraiser_name=campaign_data[0],
            goal=campaign_data[1],
            distribution_percentage=campaign_data[2],
            start_date=campaign_data[3],
            end_date=campaign_data[4],
            current_amount=campaign_data[5],
            disabled=campaign_data[6],
            created_date=campaign_data[7],
            collection_description=collection_description,
            collection_image=collection_image,
            collection_hero=collection_hero,
            owner=campaign_data[9],
            collection_address=campaign_data[10],
        )
        campaigns.append(campaign)

    return campaigns
