from pydantic import BaseModel, Field


class ChallengeReqeust(BaseModel):
    wallet_address: str = Field(..., description="Wallet address of the user")
    chain_id: int = Field(..., description="Chain of the user")


class VerificationRequest(BaseModel):
    message: str = Field(..., description="Message for the challenge")
    signature: str = Field(..., description="Signature for the challenge")


class TokenDataRequest(BaseModel):
    id: str = Field(None, description="Unique identifier for the user")
    moralis_id: str = Field(..., description="Moralis ID of the user")
    wallet_address: str = Field(..., description="Wallet address of the user")
    signature: str = Field(..., description="Signature of the user")
    chain_id: int = Field(..., description="Chain ID of the user")
