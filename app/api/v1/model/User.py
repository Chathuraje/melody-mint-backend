import re
from pydantic import BaseModel, BeforeValidator, Field, HttpUrl, EmailStr, validator
from typing import Annotated, Optional
from datetime import datetime

collection_name = "users"

PyObjectId = Annotated[str, BeforeValidator(str)]


class SocialMedia(BaseModel):
    spotify: Optional[HttpUrl] = Field(description="Spotify profile link")
    instagram: Optional[HttpUrl] = Field(description="Instagram profile link")
    youtube: Optional[HttpUrl] = Field(description="Youtube channel link")
    x: Optional[HttpUrl] = Field(description="Extra social media link")
    discord: Optional[str] = Field(description="Discord username")


class User(BaseModel):
    wallet_address: str = Field(..., description="Wallet address of the user")
    chain_id: int = Field(..., description="Chain ID of the user")
    moralis_id: str = Field(..., description="Moralis ID of the user")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    username: Optional[str] = Field(None, description="User's username")
    profile_hero: Optional[str] = Field(None, description="Profile hero image URL")
    profile_image: Optional[str] = Field(None, description="Profile image URL")
    artist_description: Optional[str] = Field(
        None, description="Description of the user"
    )
    social_media: Optional[SocialMedia] = Field(
        None, description="Social media links of the user"
    )
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    contact_no: Optional[str] = Field(None, description="Contact number of the user")
    website: Optional[HttpUrl] = Field(None, description="Website URL of the user")
    joined_date: str = Field(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="Date and time when the user joined",
    )
    disabled: Optional[bool] = Field(
        False, description="Flag to disable the user account"
    )
