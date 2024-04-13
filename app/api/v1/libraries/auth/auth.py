import traceback
from fastapi import HTTPException, status
from app.api.v1.libraries.user.db import db_create_user
from app.api.v1.model.User import User
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
from app.utils.auth import authenticate_user, create_access_token
from app.api.v1.schemas.user import UserCreateRequest
from app.api.v1.utils.common import (
    is_user_exist,
    is_valid_support_chain,
    is_valid_wallet_address,
)
from app.config import settings
from datetime import datetime, timedelta, timezone
import requests
import json
from app.utils import logging

logger = logging.getLogger()
env = settings.get_settings()


# Route: Request a Challenge Nonce for Web3 Authentication with Morals API
async def request_challenge(request: ChallengeReqeust) -> ChallengeResponse:

    if not is_valid_support_chain(request.chain_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported chain ID provided.",
        )

    if not await is_valid_wallet_address(request.wallet_address, request.chain_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid wallet address provided.",
        )

    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + "Z"

    REQUEST_URL = f"https://authapi.moralis.io/challenge/request/evm"
    request_object = {
        "domain": env.FRONTEND_APP_DOMAIN,
        "chainId": request.chain_id,
        "address": request.wallet_address,
        "statement": "Please confirm your login with Melody Mint.",
        "uri": env.FRONTEND_APP_URI,
        "expirationTime": expirationTime,
        "notBefore": "2020-01-01T00:00:00.000Z",
        "timeout": 15,
    }

    try:
        response = requests.post(
            REQUEST_URL,
            json=request_object,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-KEY": env.MORALIS_API_KEY,
            },
        )

        if response.status_code == 201:
            logger.info(f"Challenge requested for {request.wallet_address}")
            return ChallengeResponse(**json.loads(response.text))
        else:
            raise HTTPException(
                status_code=400,
                detail="Error requesting challenge nonce",
            )
    except Exception as e:
        logger.error(f"Error requesting challenge nonce: {e}")
        raise


# Route: Verify Message for Web3 Authentication with Morals API
async def verify_message(request: VerificationRequest) -> VerificationResponse:

    REQUEST_URL = f"https://authapi.moralis.io/challenge/verify/evm"
    try:
        response = requests.post(
            REQUEST_URL,
            json={"message": request.message, "signature": request.signature},
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-KEY": env.MORALIS_API_KEY,
            },
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error verifying message: {e}")
        raise HTTPException(status_code=400, detail="Error verifying message")

    if response.status_code == 201:  # user can authenticate
        address = json.loads(response.text).get("address")
        profile_id = json.loads(response.text).get("profileId")
        chain_id = json.loads(response.text).get("chainId")
        signature = request.signature

        user = await is_user_exist(address, chain_id)
        if not user:
            try:
                user_profile = UserCreateRequest(
                    wallet_address=address, chain_id=chain_id, moralis_id=profile_id
                )

                user = await db_create_user(user_profile)
                if user:
                    logger.info(f"User created. Profile ID: {profile_id}")
                else:
                    logger.error(f"Error creating user: {user}")
                    raise HTTPException(
                        status_code=500, detail="Error while creating user"
                    )

            except Exception as e:
                logger.error(f"Error creating user: {e}")
                raise HTTPException(status_code=500, detail="Error while creating user")

        jwt_user = TokenDataRequest(
            id=user.id,
            moralis_id=profile_id,
            wallet_address=address,
            signature=signature,
            chain_id=chain_id,
        )

        access_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES)
        token = create_access_token(
            jwt_user.model_dump(), expires_delta=access_token_expires
        )

        logger.info(f"User {address} authenticated. Profile ID: {profile_id}")

        response_data = {
            "id": user.id,
            "wallet_address": address,
            "chain_id": chain_id,
            "token": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return VerificationResponse(**response_data)

    elif response.status_code == 400:
        logger.error(f"Challenge not found, Timeout may have exceeded.")
        raise HTTPException(
            status_code=400,
            detail=f"Challenge not found, Timeout may have exceeded",
        )

    else:
        logger.error(
            f"Verification failed. Could not authenticate user. {response.text}"
        )
        raise HTTPException(
            status_code=401,
            detail=f"Verification failed. Could not authenticate user. {response.text}",
        )


# Route: Generate JWT Token
async def get_access_token(token_data: TokenDataRequest) -> TokenResponse:
    user = await authenticate_user(token_data)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES)
    access_token = create_access_token(
        data=token_data.model_dump(),
        expires_delta=access_token_expires,
    )

    return TokenResponse(access_token=access_token, token_type="bearer")
