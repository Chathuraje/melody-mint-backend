from typing import Optional
from pydantic import BaseModel, Field


class ChallengeResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the verification request")
    message: str = Field(
        ..., description="Message containing the details of the verification request"
    )


class VerificationResponse(BaseModel):
    id: str = Field(None, description="Unique identifier for the user profile")
    wallet_address: str = Field(None, description="Wallet address of the user")
    chain_id: Optional[int] = Field(None, description="Chain ID of the user")
    token: Optional[str] = Field(None, description="JWT access token")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    moralis_id: Optional[str] = Field(None, description="Moralis ID of the user")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of token")
