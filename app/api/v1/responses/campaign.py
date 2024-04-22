from pydantic import BaseModel, Field

from app.api.v1.model.Campaign import Campaign


class CampaignCreateResponse(BaseModel):
    campaign_data: str = Field(..., description="Campaign data")
    collection_data: str = Field(..., description="Collection data")


class CampaignsResponse(Campaign):
    pass
