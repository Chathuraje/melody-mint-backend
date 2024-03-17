from pydantic import BaseModel, Field
from typing import Optional

class InvestersList(BaseModel):
    invester_id: Optional[str] = Field(..., description="Investers list of the campaign")
    investment_amount: Optional[float] = Field(..., description="Investment amount of the campaign")
    invested_date: Optional[str] = Field(..., description="Invested data of the campaign")
    own_percentage: Optional[float] = Field(..., description="Own percentage of the campaign")
class Campaigns(BaseModel):
    title: Optional[str] = Field(..., description="Title of the campaign")
    description: Optional[str] = Field(..., description="Description of the campaign")
    title_of_the_music: Optional[str] = Field(..., description="Title of the music of the campaign")
    image: Optional[str] = Field(..., description="Image of the campaign")
    nft_image: Optional[str] = Field(..., description="NFT image of the campaign")
    start_date: Optional[str] = Field(..., description="Start date of the campaign")
    end_date: Optional[str] = Field(..., description="End date of the campaign")
    target_amount: Optional[float] = Field(..., description="Target amount of the campaign")
    distribution: Optional[int] = Field(..., description="Distribution of the campaign (%)")
    current_amount: Optional[float] = Field(..., description="Current amount of the campaign")
    created_by: Optional[str] = Field(..., description="Created by of the campaign")
    created_at: Optional[str] = Field(..., description="Created at of the campaign")
    geners: Optional[str] = Field(..., description="Geners of the campaign")
    is_active: Optional[str] = Field(..., description="Is active of the campaign")
    is_completed: Optional[str] = Field(..., description="Is completed of the campaign")
    status: Optional[str] = Field(..., description="Status of the campaign")
    investers: Optional[list[InvestersList]] = Field(..., description="Investers of the campaign")

    
class CampaignsReturn(Campaigns):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
class CampaignsNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    

class InvestCampaign(BaseModel):
    invester_id: Optional[str] = Field(..., description="Investers list of the campaign")
    amount: Optional[int] = Field(..., description="Investment amount of the campaign")
    date: Optional[str] = Field(..., description="Invested data of the campaign")
    