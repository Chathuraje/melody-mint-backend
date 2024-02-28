from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


# For Artist Only
class SocialLinks(BaseModel):
    facebook: Optional[str] = Field(..., description="Facebook Link of the artist")
    x: Optional[str] = Field(..., description="x Link of the artist")
    discord: Optional[str] = Field(..., description="Discord Link of the artist")
    spotify: Optional[str] = Field(..., description="Spotify Link of the artist")
    tiktok: Optional[str] = Field(..., description="Tiktok Link of the artist")
    
class Artist(BaseModel):
    profession: Optional[str] = Field(..., description="Profession of the artist")
    about: Optional[str] = Field(..., description="About the artist")
    social_links: Optional[list[SocialLinks]] = Field(..., description="Social links of the artist")

class Profile(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email of the user")
    contact_no: str = Field(..., description="Contact number of the user")
    profile_picture: str = Field(..., description="Profile picture of the user")

class User(BaseModel):
    wallet_address: str = Field(..., description="Wallet address of the user")
    username: str = Field(..., description="Username of the user")
    profile: Profile = Field(None, description="Profile of the user")
    is_artist: bool = Field(False, description="Indicates if the user is an artist")
    artist_data: Optional[list[Artist]]= Field(None, description="Artist data of the user")
    disabled: bool = Field(False, description="Indicates if the user is disabled")
    
class ExistingUser(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the user")


    



    
    
    
    
