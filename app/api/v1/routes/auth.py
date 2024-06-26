from fastapi import APIRouter, Request, Response
from app.api.v1.responses.auth import (
    ChallengeResponse,
    TokenResponse,
    VerificationResponse,
)
from app.api.v1.schemas.auth import (
    ChallengeReqeust,
    TokenDataRequest,
    VerificationRequest,
)
from app.utils import logging
from app.api.v1.libraries.auth import auth


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentications"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger()


@auth_router.post(
    "/request_challenge",
    description="Request a challenge to Authenticate with Web3",
    response_model=ChallengeResponse,
)
async def request_challenge(request: ChallengeReqeust):
    logger.info("Web3 Request Challenge endpoint accessed")

    return await auth.request_challenge(request)


@auth_router.post(
    "/verify_challenge",
    description="Verify the challenge to Authenticate with Web3",
    response_model=VerificationResponse,
)
async def verify_message(request: VerificationRequest, response: Response):
    logger.info("Verify message endpoint accessed.")

    return await auth.verify_message(request, response)


@auth_router.post("/access_token", response_model=TokenResponse)
async def get_access_token(
    id: str, moralis_id: str, wallet_address: str, signature: str, chain_id: int
):
    logger.info("Generate token endpoint accessed.")

    token_data = TokenDataRequest(
        id=id,
        moralis_id=moralis_id,
        wallet_address=wallet_address,
        signature=signature,
        chain_id=chain_id,
    )

    return await auth.get_access_token(token_data)


@auth_router.get("/refresh_token", response_model=TokenResponse)
async def get_refresh_token(request: Request):
    logger.info("Generate token endpoint accessed.")

    return await auth.get_refresh_token(request)


@auth_router.get("/logout", status_code=201)
async def logout(request: Request, response: Response):
    logger.info("Logout endpoint accessed.")

    return await auth.logout(request, response)
