from app.models.Marketplace import Collections, NFT, CollectionNew, CollectionsReturn, NFTNew, NFTReturn
from app.utils.response import CollectionCreateResponse, AllCollectionResponse, SingleCollectionResponse, NFTCreateResponse, AllNFTResponse, SingleNFTResponse, StandardResponse
from app.utils.database import nft_collection, marketplace_collection, user_collection
from bson import ObjectId

# SECTION: FastAPI Create NFT Collection
async def create_collection(collections: Collections) -> CollectionNew:
    return StandardResponse("Collection created successfully", 200, CollectionNew(id="123"))
# SECTION: End of FastAPI Create a new collection


# SECTION: FastAPI Get All Collections
async def get_all_collections() -> AllCollectionResponse:
    collections = []
    for collection in marketplace_collection.find():
        id=str(collection["_id"])
        collections.append(CollectionsReturn(id=id, **collection))
        
    if len(collections) == 0:
        return AllCollectionResponse(
            code=404,
            response="No collections found",
            data=None
        )
    else:
        return AllCollectionResponse(
            code=200,
            response="Collections retrieved successfully",
            data=collections
        )

# SECTION: End of FastAPI Get All Collections


# SECTION: FastAPI Get Single Collection
async def get_campaign(collection_id: str) -> SingleCollectionResponse:
    collection = marketplace_collection.find_one({"_id": ObjectId(collection_id)})
    
    if collection:
        id=str(collection["_id"])
        return SingleCollectionResponse(
            code=200,
            response="Collection retrieved successfully",
            data=CollectionsReturn(id=collection_id, **collection)
        )
    else:
        return SingleCollectionResponse(
            code=404,
            response="Collection not found",
            data=None
        )
# SECTION: End of FastAPI Get Single Collection


# SECTION: FastAPI Update Collection
async def update_collection(collection_id: str, collections: Collections) -> SingleCollectionResponse:
    result = marketplace_collection.update_one(
        {"_id": ObjectId(collection_id)},
        {"$set": collections.dict()}
    )
    if result.modified_count == 1:
        collection = marketplace_collection.find_one({"_id": ObjectId(collection_id)})
        id=str(collection["_id"])
        return SingleCollectionResponse(
            code=200,
            response="Collection updated successfully",
            data=Collections(**collection)
        )
    else:
        return SingleCollectionResponse(
            code=404,
            response="Collection not found",
            data=None
        )
# SECTION: End of FastAPI Update Collection


# SECTION: Create NFT

async def create_nft(collection_id: str, nft: NFT) -> NFTCreateResponse:
    nft_data = nft.dict()
    result = nft_collection.insert_one(nft_data)
    if result.inserted_id:
        return NFTCreateResponse(
            code=200,
            response="NFT created successfully",
            data=NFTNew(
                id=str(result.inserted_id),
            )
        )
    else:
        return NFTCreateResponse(
            code=404,
            response="NFT not created",
            data=None
        )

# SECTION: End of Create NFT


# SECTION: Get all NFts from collection id

async def get_nfts(collection_id: str) -> AllNFTResponse:
    nfts = []
    for nft in nft_collection.find({"collection_id": collection_id}):
        id=str(nft["_id"])
        nfts.append(NFTReturn(id=id, **nft))
        
    if len(nfts) == 0:
        return AllNFTResponse(
            code=404,
            response="No NFTs found",
            data=None
        )
    else:
        return AllNFTResponse(
            code=200,
            response="NFTs retrieved successfully",
            data=nfts
        )


# SECTION: End of Get all NFts from collection id


# SECTION: Get Single NFT from collection

async def get_nft(collection_id: str, nft_id: str) -> SingleNFTResponse:
    nft = nft_collection.find_one({"_id": ObjectId(nft_id), "collection_id": collection_id})
    if nft:
        id=str(nft["_id"])
        return SingleNFTResponse(
            code=200,
            response="NFT retrieved successfully",
            data=NFT(**nft)
        )
    else:
        return SingleNFTResponse(
            code=404,
            response="NFT not found",
            data=None
        )

# SECTION: End of Get Single NFT from collection


# SECTION: Update NFT
async def update_nft(collection_id: str, nft_id: str, nft: NFT) -> SingleNFTResponse:
    result = nft_collection.update_one(
        {"_id": ObjectId(nft_id), "collection_id": collection_id},
        {"$set": nft.dict()}
    )
    if result.modified_count == 1:
        nft = nft_collection.find_one({"_id": ObjectId(nft_id), "collection_id": collection_id})
        id=str(nft["_id"])
        return SingleNFTResponse(
            code=200,
            response="NFT updated successfully",
            data=NFT(**nft)
        )
    else:
        return SingleNFTResponse(
            code=404,
            response="NFT not found",
            data=None
        )
# SECTION: End of Update NFT

# SECTION: Transfer NFT
async def transfer_nft(collection_id: str, nft_id: str, owner_id: str) -> SingleNFTResponse:
    result = nft_collection.update_one(
        {"_id": ObjectId(nft_id), "collection_id": collection_id},
        {"$set": {"owner_id": owner_id}}
    )
    if result.modified_count == 1:
        nft = nft_collection.find_one({"_id": ObjectId(nft_id), "collection_id": collection_id})
        id=str(nft["_id"])
        return SingleNFTResponse(
            code=200,
            response="NFT transferred successfully",
            data=NFT(**nft)
        )
    else:
        return SingleNFTResponse(
            code=404,
            response="NFT not found",
            data=None
        )
# SECTION: End of Transfer NFT