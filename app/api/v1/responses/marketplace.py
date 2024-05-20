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
    price: float = Field(None, description="Price")


class NFTResponse(MarketplaceResponse):
    collection_owner: str = Field(..., description="Collection owner")
    nfts: list[SinglNFTResponse] = Field(None, description="NFT ID")


class SinglNFTResponseWithMarketplace(BaseModel):
    nft_id: str = Field(None, description="NFT ID")
    owner_address: str = Field(None, description="Owner address")
    collection_name: str = Field(None, description="Collection name")
    collection_symbol: str = Field(None, description="Collection symbol")
    collection_description: str = Field(None, description="Collection description")
    collection_image: str = Field(None, description="Collection image")
    collection_hero: str = Field(None, description="Collection hero")
    collection_addresse: str = Field(None, description="Collection addresse")
    collection_owner: str = Field(None, description="Collection owner")
    price: str = Field(None, description="Price")
