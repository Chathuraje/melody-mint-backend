from click import password_option
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChallengeReqeust(BaseModel):
    address: str = Field(..., description="Wallet address of the user")
    chainId: int = Field(..., description="Chain of the user")


class ChallengeResponse(BaseModel):
    id: Optional[str] = Field(
        ..., description="Unique identifier for the verification request"
    )
    message: Optional[str] = Field(
        ..., description="Message containing the details of the verification request"
    )


class VerificationRequest(BaseModel):
    message: str = Field(..., description="Message for the challenge")
    signature: str = Field(..., description="Signature for the challenge")


class VerificationResponse(BaseModel):
    id: Optional[str] = Field(
        None, description="Unique identifier for the user profile"
    )
    wallet_address: Optional[str] = Field(
        None, description="Wallet address of the user"
    )
    chain_id: Optional[int] = Field(None, description="Chain ID of the user")
    token: Optional[str] = Field(None, description="JWT access token")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of token")


class TokenData(BaseModel):
    id: str = Field(None, description="Unique identifier for the user")
    moralis_id: str = Field(..., description="Moralis ID of the user")
    wallet_address: str = Field(..., description="Wallet address of the user")
    signature: str = Field(..., description="Signature of the user")
    chain_id: int = Field(..., description="Chain ID of the user")
