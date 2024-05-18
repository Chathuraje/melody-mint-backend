from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from app.api.v1.model.User import SocialMedia, User


class UserCreateRequest(BaseModel):
    wallet_address: str = Field(..., description="Wallet address of the user")
    chain_id: int = Field(..., description="Chain ID of the user")
    moralis_id: str = Field(..., description="Moralis ID of the user")


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    username: Optional[str] = Field(None, description="user's username")
    artist_description: Optional[str] = Field(
        None, description="Description of the user"
    )
    social_media: Optional[SocialMedia] = Field(
        None, description="Social media links of the user"
    )
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    contact_no: Optional[str] = Field(None, description="Contact number of the user")
    website: Optional[str] = Field(None, description="Website URL of the user")
    disabled: Optional[bool] = Field(
        None, description="Flag to disable the user account"
    )
    verified: Optional[bool] = Field(
        None, description="Flag to verify the user account"
    )
    profile_hero: Optional[str] = Field(None, description="Profile hero image URL")
    profile_image: Optional[str] = Field(None, description="Profile image URL")
