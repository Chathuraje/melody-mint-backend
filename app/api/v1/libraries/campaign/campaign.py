import json
from typing import List
from fastapi import UploadFile
from app.api.v1.libraries.user.db import db_get_user_by_only_wallet_address
from app.utils.ipfs import pinFiletoIPFS, pinFiletoJSON, readFromIPFS
from app.api.v1.model.Campaign import CampaignOffChain, CollectionOffChain
from app.api.v1.responses.campaign import (
    CampaignCreateResponse,
    CampaignsResponse,
    InvestmentList,
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

        owner = campaign_data[9]
        owner_data = await db_get_user_by_only_wallet_address(owner)
        if owner_data is None:
            raise Exception("Failed to get owner data")

        owner_name = f"{owner_data.first_name} {owner_data.last_name}"

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
            investment=[],
            owner_name=owner_name,
        )
        campaigns.append(campaign)

    return campaigns


async def combine_similar_investments(investments: List[tuple]) -> List[InvestmentList]:
    combined_investments = {}
    for investment in investments:
        address = investment[0]
        amount = investment[1]
        if address in combined_investments:
            combined_investments[address] += amount
        else:
            combined_investments[address] = amount

    # Convert combined_investments dictionary to list of InvestmentList objects
    # Generate unique IDs for each investment
    id_counter = 1
    result = []
    for addr, amt in combined_investments.items():
        result.append(InvestmentList(id=str(id_counter), address=addr, amount=amt))
        id_counter += 1

    return result


async def get_campaign_by_id(chain_id: int, campaign_id: int) -> CampaignsResponse:
    contract = await web3_get_contract(chain_id)
    result = contract.functions.getCampaign(campaign_id).call()

    campaign_meta_data = result[8]
    data = await readFromIPFS(campaign_meta_data)
    if data is None:
        raise Exception("Failed to read from IPFS")

    collection_description = data["collection_description"]
    collection_image = data["collection_image"]
    collection_hero = data["collection_hero"]

    investmentResult = contract.functions.getCampaignInvestments(campaign_id).call()
    combined = await combine_similar_investments(investmentResult)

    owner = result[9]
    owner_data = await db_get_user_by_only_wallet_address(owner)
    if owner_data is None:
        raise Exception("Failed to get owner data")

    owner_name = f"{owner_data.first_name} {owner_data.last_name}"

    campaign = CampaignsResponse(
        fundraiser_name=result[0],
        goal=result[1],
        distribution_percentage=result[2],
        start_date=result[3],
        end_date=result[4],
        current_amount=result[5],
        disabled=result[6],
        created_date=result[7],
        collection_description=collection_description,
        collection_image=collection_image,
        collection_hero=collection_hero,
        owner=result[9],
        collection_address=result[10],
        investment=combined,
        owner_name=owner_name,
    )

    print(campaign)

    return campaign
