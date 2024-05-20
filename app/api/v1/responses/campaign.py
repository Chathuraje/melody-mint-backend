from pydantic import BaseModel, Field


class CampaignCreateResponse(BaseModel):
    campaign_data: str = Field(..., description="Campaign data")
    collection_data: str = Field(..., description="Collection data")


class InvestmentList(BaseModel):
    id: str = Field(..., description="ID")
    address: str = Field(..., description="Address of")
    amount: float = Field(..., description="Amount")


class CampaignsResponse(BaseModel):
    fundraiser_name: str = Field(..., description="Fundraiser Name")
    goal: int = Field(..., description="Goal")
    distribution_percentage: int = Field(..., description="Distribution Percentage")
    start_date: int = Field(..., description="Start Date")
    end_date: int = Field(..., description="End Date")
    current_amount: int = Field(..., description="Current Amount")
    disabled: bool = Field(..., description="Disabled")
    created_date: int = Field(..., description="Created Date")
    collection_description: str = Field(..., description="Collection Description")
    collection_image: str = Field(..., description="Collection Image")
    collection_hero: str = Field(..., description="Collection Hero")
    owner: str = Field(..., description="Owner")
    collection_address: str = Field(..., description="Collection Address")
    investment: list[InvestmentList] = Field(..., description="Investment")
    owner_name: str = Field(..., description="Owner Name")
