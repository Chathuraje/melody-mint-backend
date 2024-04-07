import traceback
from typing import Annotated
from fastapi import Depends, HTTPException, security
from app.api.auth.utils.authentication import authenticate_user, create_access_token
from app.api.user.utils import UserDbController
from app.model.Auth import ChallengeResponse, Token, TokenData, VerificationResponse
from app.model.User import UserCreateResponse, UserProfile, UserResponse
from app.utils.config import (
    JWT_EXPIRY_MINUTES,
    MORALIS_API_KEY,
    JWT_ALGORITHM,
    JWT_SECRET,
)
from datetime import datetime, timedelta, timezone
import requests
import json
from app.utils import logging
from app.utils.database import get_collection

logger = logging.getLogger()


async def request_challenge(request) -> ChallengeResponse:
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + "Z"

    REQUEST_URL = f"https://authapi.moralis.io/challenge/request/evm"
    request_object = {
        "domain": "melodymint.tech",
        "chainId": request.chainId,
        "address": request.address,
        "statement": "Please confirm your login with Melody Mint.",
        "uri": "https://defi.finance/",
        "expirationTime": expirationTime,
        "notBefore": "2020-01-01T00:00:00.000Z",
        "timeout": 15,
    }

    response = requests.post(
        REQUEST_URL, json=request_object, headers={"X-API-KEY": MORALIS_API_KEY}
    )

    return ChallengeResponse(**json.loads(response.text))


# Route: Verify Message for Web3 Authentication with Morals API
async def verify_message(request) -> VerificationResponse:
    request = request.dict()

    REQUEST_URL = f"https://authapi.moralis.io/challenge/verify/evm"
    response = requests.post(
        REQUEST_URL, json=request, headers={"X-API-KEY": MORALIS_API_KEY}
    )
    if response.status_code == 201:  # user can authenticate
        address = json.loads(response.text).get("address")
        profile_id = json.loads(response.text).get("profileId")
        chain_id = json.loads(response.text).get("chainId")
        signature = json.loads(response.text).get("signature")

        user = await UserDbController.get_user_by_wallet_address(address, chain_id)
        if not user:
            try:
                user_profile = UserProfile(
                    moralis_id=str(profile_id),
                    wallet_address=address,
                    chain_id=chain_id,
                )  # type: ignore
                user = await UserDbController.create_user(user_profile)
                if user:
                    logger.info(f"User created. Profile ID: {profile_id}")
                else:
                    logger.error(f"Error creating user: {user}")
                    raise HTTPException(
                        status_code=500, detail="Error while creating user"
                    )

            except Exception as e:
                logger.error(f"Error creating user: {e}")
                tb = traceback.format_exc()
                raise HTTPException(
                    status_code=500,
                    detail=f"Error while creating user: {e}\nTraceback: {tb}",
                ) from e

        # jwt_user = {
        #     "moralis_id": profile_id,
        #     "wallet_address": address,
        #     "signature": signature,
        # }

        # token = create_access_token(jwt_user)
        logger.info(f"User {address} authenticated. Profile ID: {profile_id}")

        return VerificationResponse(id=user.id)  # type: ignore

    else:
        logger.error("User not authenticated")
        raise HTTPException(status_code=401, detail="User not authenticated")


# Route: Generate JWT Token
async def login_for_access_token(token_data: TokenData):
    user = authenticate_user(token_data)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=JWT_EXPIRY_MINUTES)
    access_token = create_access_token(
        data=token_data.model_dump(),
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
