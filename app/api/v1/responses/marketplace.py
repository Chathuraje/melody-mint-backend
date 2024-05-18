from pydantic import BaseModel, Field


class MarketplaceResponse(BaseModel):
    collection_name: str = Field(..., description="Collection name")
    collection_symbol: str = Field(..., description="Collection symbol")
    collection_description: str = Field(..., description="Collection description")
    collection_image: str = Field(..., description="Collection image")
    collection_hero: str = Field(..., description="Collection hero")
    collection_addresse: str = Field(..., description="Collection addresse")


class SinglNFTResponse(BaseModel):
    nft_id: str = Field(None, description="NFT ID")
    owner_address: str = Field(None, description="Owner address")


class NFTResponse(MarketplaceResponse):
    collection_owner: str = Field(..., description="Collection owner")
    nfts: list[SinglNFTResponse] = Field(None, description="NFT ID")
