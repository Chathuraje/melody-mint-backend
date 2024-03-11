from app.utils.response import CampaignCreateResponse, SingleCampaignResponse, AllCampaignResponse, InvestmentResponse
from app.models.Campaigns import Campaigns, CampaignsReturn, CampaignsNew
from app.utils.database import user_collection, campaign_collection
from bson import ObjectId
from app.models.Campaigns import Campaigns, InvestCampaign


# SECTION: FastAPI Create a new campaign
async def create_campaign(campaign: Campaigns) -> CampaignsNew:
    campaign_data = campaign.dict()
    result = campaign_collection.insert_one(campaign_data)
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
# SECTION: End of FastAPI Create a new campaign

# SECTION: Get Fastapi all campaigns
async def get_all_campaigns() -> AllCampaignResponse:
    campaigns = campaign_collection.find()
    individual_campaign_responses = []
    for campaign_data in campaigns:
        campaign_id = str(campaign_data['_id'])
        campaign = CampaignsReturn(
            id=campaign_id,
            title=campaign_data.get('title'),
            description=campaign_data.get('description'),
            title_of_the_music=campaign_data.get('title_of_the_music'),
            image=campaign_data.get('image'),
            nft_image=campaign_data.get('nft_image'),
            start_date=campaign_data.get('start_date'),
            end_date=campaign_data.get('end_date'),
            target_amount=campaign_data.get('target_amount'),
            distribution=campaign_data.get('distribution'),
            current_amount=campaign_data.get('current_amount'),
            created_by=campaign_data.get('created_by'),
            created_at=campaign_data.get('created_at'),
            geners=campaign_data.get('geners'),
            is_active=campaign_data.get('is_active'),
            is_released=campaign_data.get('is_released'),
            is_completed=campaign_data.get('is_completed'),
            status=campaign_data.get('status'),
            investers_list=campaign_data.get('investers_list'),
            investment_amount=campaign_data.get('investment_amount'),
            invested_date=campaign_data.get('invested_date'),
            own_percentage=campaign_data.get('own_percentage')
        )
        individual_campaign_responses.append(campaign)

    # Create AllCampaignResponse
    return AllCampaignResponse(
        code=200,
        response=f"{len(individual_campaign_responses)} Campaigns found",
        data=individual_campaign_responses
    )
# SECTION: End of FastAPI Get all campaigns

# SECTION: Get Single Campaign from Campaign id
async def get_campaign(campaign_id: str) -> SingleCampaignResponse:
    campaign_data = campaign_collection.find_one({"_id": ObjectId(campaign_id)})
    if campaign_data:
        campaign = CampaignsReturn(
            id=str(campaign_data['_id']),
            title=campaign_data.get('title'),
            description=campaign_data.get('description'),
            title_of_the_music=campaign_data.get('title_of_the_music'),
            image=campaign_data.get('image'),
            nft_image=campaign_data.get('nft_image'),
            start_date=campaign_data.get('start_date'),
            end_date=campaign_data.get('end_date'),
            target_amount=campaign_data.get('target_amount'),
            distribution=campaign_data.get('distribution'),
            current_amount=campaign_data.get('current_amount'),
            created_by=campaign_data.get('created_by'),
            created_at=campaign_data.get('created_at'),
            geners=campaign_data.get('geners'),
            is_active=campaign_data.get('is_active'),
            is_released=campaign_data.get('is_released'),
            is_completed=campaign_data.get('is_completed'),
            status=campaign_data.get('status'),
            investers_list=campaign_data.get('investers_list'),
            investment_amount=campaign_data.get('investment_amount'),
            invested_date=campaign_data.get('invested_date'),
            own_percentage=campaign_data.get('own_percentage')
        )
        return SingleCampaignResponse(
            code=200,
            response="Campaign found",
            data=campaign
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
async def invest_campaign(campaign_id: str, investment_details: InvestCampaign) -> InvestmentResponse:
    campaign_data = campaign_collection.find_one({"_id": ObjectId(campaign_id)})
    if campaign_data:
        current_amount = int(campaign_data.get('current_amount'))
        target_amount = int(campaign_data.get('target_amount'))
        
        invester_id = str(investment_details.invester_id)
        amount = int(investment_details.amount)
        date = str(investment_details.date)
        
        # calculate own percentage after invest
        percentage = (investment_amount / target_amount) * 100
        
        if current_amount is None:
            current_amount = 0
        current_amount += amount
        
        user_id_obj = ObjectId(invester_id)
        user_data = user_collection.find_one({"_id": ObjectId(user_id_obj)})  
       
        if user_data:
            investers_list = campaign_data.get('investers_list')
            investment_amount = campaign_data.get('investment_amount')
            invested_date = campaign_data.get('invested_date')
            own_percentage = campaign_data.get('own_percentage')
            
            # if invester_id in investers_list:
            #     # Update investment amount for existing investor
            #     index = investers_list.index(invester_id)
            #     investment_amount[index] += amount
            # else:
            #     # Append new investor and investment amount
            #     investers_list.append(invester_id)
            #     investment_amount.append(amount)
            
            investers_list.append(invester_id)
            investment_amount.append(amount)
            invested_date.append(date)
            own_percentage.append(percentage)
            
            campaign_id_obj = ObjectId(campaign_id)
            result = campaign_collection.update_one({"_id": ObjectId(campaign_id_obj)}, {"$set": {"current_amount": current_amount, "investers_list": investers_list, "investment_amount": investment_amount, "invested_date": invested_date, "own_percentage": own_percentage}})
            if result.modified_count == 1:
                return InvestmentResponse(
                    code=200,
                    response="Investment Successful",
                    data=None
                )
            else:
                return InvestmentResponse(
                    code=404,
                    response="Investment not Updated",
                    data=None
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
    user_campaigns = campaign_collection.find({"created_by": user_id})
    individual_campaign_responses = []
    for campaign_data in user_campaigns:
        campaign_id = str(campaign_data['_id'])
        campaign = CampaignsReturn(
            id=campaign_id,
            title=campaign_data.get('title'),
            description=campaign_data.get('description'),
            title_of_the_music=campaign_data.get('title_of_the_music'),
            image=campaign_data.get('image'),
            nft_image=campaign_data.get('nft_image'),
            start_date=campaign_data.get('start_date'),
            end_date=campaign_data.get('end_date'),
            target_amount=campaign_data.get('target_amount'),
            distribution=campaign_data.get('distribution'),
            current_amount=campaign_data.get('current_amount'),
            created_by=campaign_data.get('created_by'),
            created_at=campaign_data.get('created_at'),
            geners=campaign_data.get('geners'),
            is_active=campaign_data.get('is_active'),
            is_released=campaign_data.get('is_released'),
            is_completed=campaign_data.get('is_completed'),
            status=campaign_data.get('status'),
            investers_list=campaign_data.get('investers_list'),
            investment_amount=campaign_data.get('investment_amount'),
            invested_date=campaign_data.get('invested_date'),
            own_percentage=campaign_data.get('own_percentage')
        )
        individual_campaign_responses.append(campaign)

    # Create AllCampaignResponse
    return AllCampaignResponse(
        code=200,
        response=f"{len(individual_campaign_responses)} Campaigns found",
        data=individual_campaign_responses
    )

# SECTION: End of Get User Campaigns


# SECTION: Get User Investments
async def get_investments(user_id: str) -> AllCampaignResponse:
    user_investments = campaign_collection.find({"investers_list": user_id})
    individual_campaign_responses = []
    for campaign_data in user_investments:
        campaign_id = str(campaign_data['_id'])
        campaign = CampaignsReturn(
            id=campaign_id,
            title=campaign_data.get('title'),
            description=campaign_data.get('description'),
            title_of_the_music=campaign_data.get('title_of_the_music'),
            image=campaign_data.get('image'),
            nft_image=campaign_data.get('nft_image'),
            start_date=campaign_data.get('start_date'),
            end_date=campaign_data.get('end_date'),
            target_amount=campaign_data.get('target_amount'),
            distribution=campaign_data.get('distribution'),
            current_amount=campaign_data.get('current_amount'),
            created_by=campaign_data.get('created_by'),
            created_at=campaign_data.get('created_at'),
            geners=campaign_data.get('geners'),
            is_active=campaign_data.get('is_active'),
            is_released=campaign_data.get('is_released'),
            is_completed=campaign_data.get('is_completed'),
            status=campaign_data.get('status'),
            investers_list=campaign_data.get('investers_list'),
            investment_amount=campaign_data.get('investment_amount'),
            invested_date=campaign_data.get('invested_date'),
            own_percentage=campaign_data.get('own_percentage')
        )
        individual_campaign_responses.append(campaign)

    # Create AllCampaignResponse
    return AllCampaignResponse(
        code=200,
        response=f"{len(individual_campaign_responses)} Investments found",
        data=individual_campaign_responses
    )
# SECTION: End of Get User Investments