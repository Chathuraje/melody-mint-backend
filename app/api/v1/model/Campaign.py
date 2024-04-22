from pydantic import BaseModel, Field


class CampaignBlockchain(BaseModel):
    fundraiser_name: str = Field(..., description="Name of the fundraiser")
    goal: int = Field(..., description="Goal amount of the fundraiser")
    distribution_percentage: float = Field(..., description="Distribution percentage")
    start_date: str = Field(..., description="Start date of the fundraiser")
    end_date: str = Field(..., description="End date of the fundraiser")
    current_amount: int = Field(..., description="Current amount of the fundraiser")
    disabled: bool = Field(..., description="Disabled flag for this campaign")
    created_date: str = Field(
        ..., description="Date and time when the campaign was created"
    )
    owner: str = Field(..., description="Owner of the campaign")

    creation_name: str = Field(..., description="Name of the creation")
    creation_description: str = Field(..., description="Description of the creation")


class CampaignOffChain(BaseModel):
    description: str = Field(..., description="Description of the campaign")
    short_description: str = Field(..., description="Short description of the campaign")
    image: str = Field(None, description="Image URL of the campaign")


class CollectionOffChain(BaseModel):
    collection_description: str = Field(
        ..., description="Description of the collection"
    )
    creation_image: str = Field(None, description="Creation image URL")
    creation_hero: str = Field(None, description="Creation hero URL")


class Campaign(CampaignBlockchain, CampaignOffChain):
    pass
