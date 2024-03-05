from app.utils.response import AllCampaignResponse
from app.models.Campaigns import CampaignsReturn
from app.utils.database import user_collection, campaign_collection

# SECTION: Get Fastapi all campaigns
async def get_all_campaigns():
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
            investment_amount=campaign_data.get('investment_amount')
        )
        individual_campaign_responses.append(campaign)

    # Create AllCampaignResponse
    return AllCampaignResponse(
        code=200,
        response=f"{len(individual_campaign_responses)} Campaigns found",
        data=individual_campaign_responses
    )
# SECTION: End of FastAPI Get all campaigns