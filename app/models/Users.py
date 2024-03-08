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
    social_links: Optional[SocialLinks] = Field(..., description="Social links of the artist")

class Profile(BaseModel):
    first_name: Optional[str] = Field(..., description="First name of the user")
    last_name: Optional[str] = Field(..., description="Last name of the user")
    email: Optional[str] = Field(..., description="Email of the user")
    contact_no: Optional[str] = Field(..., description="Contact number of the user")
    country: Optional[str] = Field(..., description="Country of the user")
    state: Optional[str] = Field(..., description="State of the user")
    profile_picture: Optional[str] = Field(..., description="Profile picture of the user")

class User(BaseModel):
    wallet_address: Optional[str] = Field(..., description="Wallet address of the user")
    hash_password: Optional[str] = Field(..., description="Hashed password of the user")
    username: Optional[str] = Field(..., description="Username of the user")
    profile: Optional[Profile] = Field(None, description="Profile of the user")
    is_artist: Optional[bool] = Field(False, description="Indicates if the user is an artist")
    artist_data: Optional[Artist]= Field(None, description="Artist data of the user")
    disabled: Optional[bool] = Field(False, description="Indicates if the user is disabled")
    
class ExistingUser(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the user")
    
class UserReturn(User):
    id: Optional[str] = Field(..., description="Unique ID of the user")

# class Token(BaseModel):
#     access_token: str
#     token_type: str
    
# class TokenData(BaseModel):
#     wallet_address: str = None
    
# class UserInDB(User):
#     hash_password: str

    



    
    
    
    
