from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Optional
from datetime import datetime

collection_name = "users"

PyObjectId = Annotated[str, BeforeValidator(str)]


class SocialMedia(BaseModel):
    spotify: Optional[str] = Field(None, description="Spotify profile link")
    instagram: Optional[str] = Field(None, description="Instagram profile link")
    youtube: Optional[str] = Field(None, description="Youtube channel link")
    x: Optional[str] = Field(None, description="Extra social media link")
    discord: Optional[str] = Field(None, description="Discord username")


class UserProfile(BaseModel):
    username: Optional[str] = Field(None, description="user's username")
    profile_hero: Optional[str] = Field(None, description="Profile hero image URL")
    profile_image: Optional[str] = Field(None, description="Profile image URL")
    artist_description: Optional[str] = Field(
        None, description="Description of the user"
    )
    social_media: Optional[SocialMedia] = Field(
        None, description="Social media links of the user"
    )
    wallet_address: str = Field(..., description="Wallet address of the user")
    chain_id: int = Field(..., description="Chain ID of the user")
    moralis_id: str = Field(..., description="Moralis ID of the user")
    email: Optional[str] = Field(None, description="Email address of the user")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    contact_no: Optional[str] = Field(None, description="Contact number of the user")
    website: Optional[str] = Field(None, description="Website URL of the user")
    joined_date: str = Field(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="Date and time when the user joined",
    )


class UserResponse(UserProfile):
    id: PyObjectId = Field(..., description="user's ID")


class UserCreateResponse(BaseModel):
    id: PyObjectId = Field(..., description="user's ID")
