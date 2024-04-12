from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from app.api.v1.model.User import SocialMedia, User


class UserCreateRequest(BaseModel):
    wallet_address: str = Field(..., description="Wallet address of the user")
    chain_id: int = Field(..., description="Chain ID of the user")
    moralis_id: str = Field(..., description="Moralis ID of the user")


class UserUpdateRequest(BaseModel):
    first_name: str = Field("", description="First name")
    last_name: str = Field("", description="Last name")
    username: str = Field("", description="user's username")
    profile_hero: HttpUrl = Field("", description="Profile hero image URL")
    profile_image: HttpUrl = Field("", description="Profile image URL")
    artist_description: str = Field("", description="Description of the user")
    social_media: SocialMedia = Field("", description="Social media links of the user")
    email: EmailStr = Field("", description="Email address of the user")
    contact_no: str = Field("", description="Contact number of the user")
    website: HttpUrl = Field("", description="Website URL of the user")
    disabled: bool = Field(False, description="Flag to disable the user account")
