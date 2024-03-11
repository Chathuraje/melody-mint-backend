from app.models.Marketplace import Collections, NFT, CollectionNew, CollectionsReturn
from app.utils.response import CollectionCreateResponse, AllCampaignResponse, SingleCampaignResponse
from app.utils.database import user_collection, marketplace_collection
from bson import ObjectId

# SECTION: FastAPI Create NFT Collection
async def create_collection(collections: Collections) -> CollectionNew:
    campaign_data = collections.dict()
    result = marketplace_collection.insert_one(campaign_data)
    if result.inserted_id:
        return CollectionCreateResponse(
            code=200,
            response="Campaign created successfully",
            data=CollectionNew(
                id=str(result.inserted_id),
            )
        )
    else:
        return CollectionCreateResponse(
            code=404,
            response="Campaign not created",
            data=None
        )
# SECTION: End of FastAPI Create a new collection


# SECTION: FastAPI Get All Collections
async def get_all_collections() -> SingleCampaignResponse:
    collections = []
    for collection in marketplace_collection.find():
        id=str(collection["_id"])
        collections.append(CollectionsReturn(id=id, **collection))
        
    if len(collections) == 0:
        return AllCampaignResponse(
            code=404,
            response="No collections found",
            data=None
        )
    else:
        return AllCampaignResponse(
            code=200,
            response="Collections retrieved successfully",
            data=collections
        )

# SECTION: End of FastAPI Get All Collections


# SECTION: FastAPI Get Single Collection
async def get_campaign(collection_id: str) -> SingleCampaignResponse:
    collection = marketplace_collection.find_one({"_id": ObjectId(collection_id)})
    if collection:
        id=str(collection["_id"])
        return SingleCampaignResponse(
            code=200,
            response="Collection retrieved successfully",
            data=Collections(**collection)
        )
    else:
        return SingleCampaignResponse(
            code=404,
            response="Collection not found",
            data=None
        )
# SECTION: End of FastAPI Get Single Collection