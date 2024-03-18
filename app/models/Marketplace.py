from pydantic import BaseModel, Field
from typing import Optional

class Collections(BaseModel):
    name: Optional[str] = Field(..., description="Name of the Collection")
    description: Optional[str] = Field(..., description="Description of the Collection")
    owner_id: Optional[str] = Field(..., description="Owner of the Collection")
    campaign_id: Optional[str] = Field(..., description="Campaign ID of the Collection")
    
class CollectionNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")

class CollectionsReturn(Collections):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    owner_name: Optional[str] = Field(..., description="Owner Name of the Collection")
    floor: Optional[str] = Field(..., description="Flor of the Collection")
    volume: Optional[str] = Field(..., description="Volume of the Collection")
    
    
class NFT(BaseModel):
    collection_id: Optional[str] = Field(..., description="Collection ID of the NFT")
    token_name: Optional[str] = Field(..., description="Name of the NFT")
    token_description: Optional[str] = Field(..., description="Description of the NFT")
    image: Optional[str] = Field(..., description="Image of the NFT")
    owner_id: Optional[str] = Field(..., description="Owner of the NFT")
    current_owner_id: Optional[str] = Field(..., description="Current Owner of the NFT")
    creation_date: Optional[str] = Field(..., description="Creation Date of the NFT")
    royalties: Optional[str] = Field(..., description="Royalties of the NFT")
    price: Optional[str] = Field(..., description="Price of the NFT")
    status: Optional[str] = Field(..., description="Status of the NFT")
    
class NFTNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")

class NFTReturn(NFT):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
    
class Transactions(BaseModel):
    sender_id: Optional[str] = Field(..., description="Sender ID of the Transaction")
    receiver_id: Optional[str] = Field(..., description="Receiver ID of the Transaction")
    amount: Optional[str] = Field(..., description="Amount of the Transaction")
    timespan: Optional[str] = Field(..., description="Timespan of the Transaction")
    Transaction_type: Optional[str] = Field(..., description="Type of the Transaction")
    nft_token_id: Optional[str] = Field(..., description="NFT Token ID of the Transaction")
    

    