from app.utils.response import CampaignCreateResponse, SingleCampaignResponse, AllCampaignResponse, InvestmentResponse
from app.models.Campaigns import Campaigns, CampaignsReturn, CampaignsNew, InvesterCampaign
from app.utils.database import marketplace_collection, user_collection, campaign_collection, nft_collection
from bson import ObjectId
from app.models.Campaigns import Campaigns, InvestersList
from app.models.Marketplace import NFT
import time
import datetime

# SECTION: FastAPI Create a new campaign
async def create_campaign(campaign: Campaigns) -> CampaignsNew:
    campaign_data = campaign.dict()
    
    artist_id = campaign_data['created_by']
    user = user_collection.find_one({"_id": ObjectId(artist_id)})
    
    if user is None:
        return CampaignCreateResponse(
            code=404,
            response="User not found",
            data=None
        )
    campaign_data["created_at"] = time.strftime("%Y-%m-%d")
    campaign_data['creater_name'] = user['first_name'] + " " + user['last_name']
    result = campaign_collection.insert_one(campaign_data)
    
    if result.inserted_id:
        collection_data = {}
        
        collection_data['name'] = campaign_data['title']
        collection_data['description'] = campaign_data['description']
        collection_data['owner_id'] = artist_id
        collection_data['owner_name'] = campaign_data['creater_name']
        collection_data['floor'] = "12.9"
        collection_data['volume'] = "125"
        collection_data['campaign_id'] = str(result.inserted_id)
            
        result = marketplace_collection.insert_one(collection_data)
        if result.inserted_id:
            return CampaignCreateResponse(
                code=200,
                response="Campaign created successfully",
                data=CampaignsNew(
                    id=str(result.inserted_id),
                )
            )
        else:
            return CampaignCreateResponse(
                code=404,
                response="Campaign not created",
                data=None
            )
    else:
        return CampaignCreateResponse(
            code=404,
            response="Campaign not created",
            data=None
        )
        
# SECTION: End of FastAPI Create a new campaign

# SECTION: Get Fastapi all campaigns
async def get_all_campaigns() -> AllCampaignResponse:
    campaigns = []
    for campaign in campaign_collection.find():
        id=str(campaign["_id"])
        campaigns.append(CampaignsReturn(id=id, **campaign))
        
    if len(campaigns) == 0:
        return AllCampaignResponse(
            code=404,
            response="No Campaign found",
            data=None
        )
    else:
        return AllCampaignResponse(
            code=200,
            response=f"{len(campaigns)} Campaigns found",
            data=campaigns
        )
# SECTION: End of FastAPI Get all campaigns

# SECTION: Get Single Campaign from Campaign id
async def get_campaign(campaign_id: str) -> SingleCampaignResponse:
    campaign_data = campaign_collection.find_one({"_id": ObjectId(campaign_id)})
    if campaign_data:
        id=str(campaign_data["_id"])
        return SingleCampaignResponse(
            code=200,
            response="Campaign retrieved successfully",
            data=Campaigns(**campaign_data)
        )
    else:
        return SingleCampaignResponse(
            code=404,
            response="Campaign not found",
            data=None
        )
    
# SECTION: End of get Single Campaign from Campaign id


# SECTION: Update Campaign from Campaign id
async def update_campaign(campaign_id: str, campaign: Campaigns) -> SingleCampaignResponse:
    campaign_id_obj = ObjectId(campaign_id)
    campaign_data = campaign.dict()
    result = campaign_collection.update_one({"_id": ObjectId(campaign_id_obj)}, {"$set": campaign_data})
    if result.modified_count == 1:
        return SingleCampaignResponse(
            code=200,
            response="Campaign Updated",
            data=campaign_data
        )
    else:
        return SingleCampaignResponse(
            code=404,
            response="Campaign not Updated",
            data=None
        )
# SECTION: End of Update Campaign from Campaign id



# SECTION: Invest to the Campaign
async def invest_campaign(campaign_id: str, investment_details: InvestersList) -> InvestmentResponse:
    campaign_data = campaign_collection.find_one({"_id": ObjectId(campaign_id)})
    if campaign_data:
        current_amount = int(campaign_data.get('current_amount'))
        target_amount = int(campaign_data.get('target_amount'))
        
        invester_id = str(investment_details.invester_id)
        amount = int(investment_details.investment_amount)
        date = time.strftime("%Y-%m-%d")
        
        # calculate own percentage after invest
        percentage = (amount / target_amount) * 100
        percentage = round(percentage)

        if current_amount is None:
            current_amount = 0
        current_amount += amount
        
        user_id_obj = ObjectId(invester_id)
        user_data = user_collection.find_one({"_id": ObjectId(user_id_obj)})  
       
        if user_data:
            # Update campaign data
            campaign_collection.update_one(
                {"_id": ObjectId(campaign_id)},
                {
                    "$push": {
                        "investers": {
                            "invester_id": invester_id,
                            "investment_amount": amount,
                            "invested_date": date,
                            "own_percentage": percentage,
                            "invester_name": user_data['first_name'] + " " + user_data['last_name']
                        }
                    },
                    "$set": {
                        "current_amount": current_amount
                    }
                }
            )
        
            marketplace_data = marketplace_collection.find_one({"campaign_id": campaign_id})
            timestamp = int(time.time())
            nft_data = {
                'collection_id': str(marketplace_data['_id']),
                "token_name": f"{campaign_data['title']}_{timestamp}",
                "token_description": campaign_data['description'],
                "image": campaign_data['image'],
                "owner_id": campaign_data['created_by'],
                "current_owner_id": invester_id,
                "creation_date": date,
                "royalties": percentage,
                "price": "0",
                "status": "active"
            }
            
            
            nfts = nft_collection.insert_one(nft_data)
            
            if nfts.inserted_id:
                campaign_data = campaign_collection.find_one({"_id": ObjectId(campaign_id)})
                return InvestmentResponse(
                    code=200,
                    response="Investment successful",
                    data=CampaignsReturn(id=campaign_id, **campaign_data)
                )
        else:
            return InvestmentResponse(
                code=404,
                response="User not found",
                data=None
            )
    else:
        return InvestmentResponse(
            code=404,
            response="Campaign not found",
            data=None
        )
# SECTION: End of Invest to the Campaign


# SECTION: Get User Campaigns
async def get_user_campaigns(user_id: str) -> AllCampaignResponse:
    user_campaigns = []
    for campaign in campaign_collection.find({"created_by": user_id}):
        id=str(campaign["_id"])
        user_campaigns.append(CampaignsReturn(id=id, **campaign))
        
    if len(user_campaigns) == 0:
        return AllCampaignResponse(
            code=404,
            response="No Campaign found",
            data=None
        )
    else:
        return AllCampaignResponse(
            code=200,
            response=f"{len(user_campaigns)} Campaigns found",
            data=user_campaigns
        )
# SECTION: End of Get User Campaigns


# SECTION: Get User Investments
async def get_investments(user_id: str) -> AllCampaignResponse:
    campaign_data = campaign_collection.find()
    
    user_investments = []
    ids = []
    for campaign in campaign_data:
        for investers in campaign['investers']:
            if investers['invester_id'] == user_id:
                if str(campaign["_id"]) in ids:
                    continue
                
                user_investments.append(InvesterCampaign(id=str(campaign["_id"]), **campaign))
                ids.append(str(campaign["_id"]))
        
    if len(user_investments) == 0:
        return AllCampaignResponse(
            code=404,
            response="No Investments found",
            data=None
        )
    else:
        return AllCampaignResponse(
            code=200,
            response=f"{len(user_investments)} Investments found",
            data=user_investments
        )
# SECTION: End of Get User Investments