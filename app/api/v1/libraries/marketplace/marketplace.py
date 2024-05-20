from app.api.v1.responses.marketplace import (
    MarketplaceResponse,
    NFTResponse,
    SinglNFTResponse,
    SinglNFTResponseWithMarketplace,
)
from app.utils.ipfs import readFromIPFS
from config.web3 import web3_get_collection_contract, web3_get_contract


async def get_marketplace(chain_id: int) -> list[MarketplaceResponse]:
    contract = await web3_get_contract(chain_id)
    result = contract.functions.getAllCampaigns().call()

    collections = []
    for collections_data in result:
        collection_address = collections_data[10]
        collection_result = contract.functions.getCollectionByCollectionAddress(
            collection_address
        ).call()

        collection_metadata = collection_result[2]

        collection_data = await readFromIPFS(collection_metadata)
        collection_description = collection_data["collection_description"]
        collection_image = collection_data["collection_image"]
        collection_hero = collection_data["collection_hero"]

        collecton = MarketplaceResponse(
            collection_name=collection_result[0],
            collection_symbol=collection_result[1],
            collection_description=collection_description,
            collection_image=collection_image,
            collection_hero=collection_hero,
            collection_addresse=collection_address,
        )

        collections.append(collecton)

    return collections


async def get_nfts(chain_id: int, collection_address: str) -> NFTResponse:
    contract_collection = await web3_get_contract(chain_id)
    result_collection = contract_collection.functions.getCollectionByCollectionAddress(
        collection_address
    ).call()

    collection_name = result_collection[0]
    collection_symbol = result_collection[1]
    collection_metadata = result_collection[2]
    collection_addresse = result_collection[3]
    collection_owner = result_collection[4]

    collection_data = await readFromIPFS(collection_metadata)
    collection_description = collection_data["collection_description"]
    collection_image = collection_data["collection_image"]
    collection_hero = collection_data["collection_hero"]

    all_nfts = {
        "collection_name": collection_name,
        "collection_symbol": collection_symbol,
        "collection_description": collection_description,
        "collection_image": collection_image,
        "collection_hero": collection_hero,
        "collection_addresse": collection_addresse,
        "collection_owner": collection_owner,
        "nfts": [],
    }

    contract_nft = await web3_get_collection_contract(chain_id, collection_address)
    result_nft = contract_nft.functions.getAllNFTsWithOwners().call()

    for nft_info in result_nft:
        owner_address, nft_id = nft_info
        nft = SinglNFTResponse(nft_id=str(nft_id), owner_address=owner_address, price=0)
        all_nfts["nfts"].append(nft)

    return NFTResponse(**all_nfts)


async def get_single_nft(
    chain_id: int, collection_address: str, nft_id: str
) -> SinglNFTResponseWithMarketplace:
    contract_collection = await web3_get_contract(chain_id)
    result_collection = contract_collection.functions.getCollectionByCollectionAddress(
        collection_address
    ).call()

    collection_name = result_collection[0]
    collection_symbol = result_collection[1]
    collection_metadata = result_collection[2]
    collection_addresse = result_collection[3]
    collection_owner = result_collection[4]

    collection_data = await readFromIPFS(collection_metadata)
    collection_description = collection_data["collection_description"]
    collection_image = collection_data["collection_image"]
    collection_hero = collection_data["collection_hero"]

    contract = await web3_get_collection_contract(chain_id, collection_address)
    result = contract.functions.getSingleNFT(int(nft_id)).call()
    print(result)
    nft = {
        "collection_name": collection_name,
        "collection_symbol": collection_symbol,
        "collection_description": collection_description,
        "collection_image": collection_image,
        "collection_hero": collection_hero,
        "collection_addresse": collection_addresse,
        "collection_owner": collection_owner,
        "nft_id": nft_id,
        "owner_address": result[0],
        "price": str(result[2]),
    }

    return SinglNFTResponseWithMarketplace(**nft)
