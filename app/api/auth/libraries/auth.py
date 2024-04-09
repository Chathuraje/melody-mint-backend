import traceback
from fastapi import HTTPException
from app.api.auth.utils.authentication import authenticate_user, create_access_token
from app.api.user.utils import UserDbController
from app.model.Auth import (
    ChallengeReqeust,
    ChallengeResponse,
    TokenResponse,
    TokenData,
    VerificationRequest,
    VerificationResponse,
)
from app.model.User import UserProfile
from app.utils.config import (
    JWT_EXPIRY_MINUTES,
    MORALIS_API_KEY,
    APP_DOMAIN,
    APP_URI,
)
from datetime import datetime, timedelta, timezone
import requests
import json
from app.utils import logging

logger = logging.getLogger()


# Route: Request a Challenge Nonce for Web3 Authentication with Morals API
async def request_challenge(request: ChallengeReqeust) -> ChallengeResponse:
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + "Z"

    REQUEST_URL = f"https://authapi.moralis.io/challenge/request/evm"
    request_object = {
        "domain": APP_DOMAIN,
        "chainId": request.chainId,
        "address": request.address,
        "statement": "Please confirm your login with Melody Mint.",
        "uri": APP_URI,
        "expirationTime": expirationTime,
        "notBefore": "2020-01-01T00:00:00.000Z",
        "timeout": 15,
    }

    response = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": MORALIS_API_KEY,
        },
    )

    return ChallengeResponse(**json.loads(response.text))


# Route: Verify Message for Web3 Authentication with Morals API
async def verify_message(request: VerificationRequest) -> VerificationResponse:

    REQUEST_URL = f"https://authapi.moralis.io/challenge/verify/evm"
    response = requests.post(
        REQUEST_URL,
        json={"message": request.message, "signature": request.signature},
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": MORALIS_API_KEY,
        },
    )

    if response.status_code == 201:  # user can authenticate
        address = json.loads(response.text).get("address")
        profile_id = json.loads(response.text).get("profileId")
        chain_id = json.loads(response.text).get("chainId")
        signature = request.signature

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

        jwt_user = TokenData(
            id=user.id,
            moralis_id=profile_id,
            wallet_address=address,
            signature=signature,
            chain_id=chain_id,
        )

        access_token_expires = timedelta(minutes=JWT_EXPIRY_MINUTES)
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
async def get_access_token(token_data: TokenData):
    user = await authenticate_user(token_data)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=JWT_EXPIRY_MINUTES)
    access_token = create_access_token(
        data=token_data.model_dump(),
        expires_delta=access_token_expires,
    )

    return TokenResponse(access_token=access_token, token_type="bearer")
