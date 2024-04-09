from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, security
from app.api.auth.utils.authentication import get_current_user
from app.model.User import UserProfile
from app.utils import logging
from app.api.auth.libraries import auth
from app.model.Auth import (
    ChallengeReqeust,
    ChallengeResponse,
    Token,
    TokenData,
    VerificationRequest,
    VerificationResponse,
)


logger = logging.getLogger()
router = APIRouter()

user_dependacy = Annotated[dict, Depends(get_current_user)]


@router.post(
    "/request_challenge",
    description="Request a challenge to Authenticate with Web3",
    response_model=ChallengeResponse,
)
async def request_challenge(request: ChallengeReqeust):
    logger.info("Web3 Request Challenge endpoint accessed")

    return await auth.request_challenge(request)


@router.post(
    "/verify_challenge",
    description="Verify the challenge to Authenticate with Web3",
    response_model=VerificationResponse,
)
async def verify_message(request: VerificationRequest):
    logger.info("Verify message endpoint accessed.")

    return await auth.verify_message(request)


@router.post("/token", response_model=Token)
async def get_access_token(
    moralis_id: str, wallet_address: str, signature: str, chain_id: int
):
    logger.info("Generate token endpoint accessed.")

    token_data = TokenData(
        moralis_id=moralis_id,
        wallet_address=wallet_address,
        signature=signature,
        chain_id=chain_id,
    )

    return await auth.get_access_token(token_data)


@router.get("/protected_route")
async def protected_route(user: user_dependacy):
    return user
