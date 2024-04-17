from os import access
from fastapi import HTTPException, Request, Response, status
from jose import JWTError, jwt
from app.api.v1.libraries.user.db import (
    db_create_user,
    db_delete_stored_message,
    db_store_message,
)
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
from app.utils.auth import authenticate_user, create_access_token, create_refresh_token
from app.api.v1.schemas.user import UserCreateRequest
from app.api.v1.utils.common import (
    is_user_exist,
    is_valid_support_chain,
    is_valid_wallet_address,
)
from config import settings
from datetime import datetime, timedelta, timezone
import requests
import json
from app.utils import logging
from app.api.v1.libraries.auth import auth

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
async def verify_message(
    request: VerificationRequest, response: Response
) -> VerificationResponse:

    REQUEST_URL = f"https://authapi.moralis.io/challenge/verify/evm"
    try:
        moralis_response = requests.post(
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

    if moralis_response.status_code == 201:  # user can authenticate
        # Store message and the wallet address in the database
        wallet_address = json.loads(moralis_response.text).get("address")
        moralis_id = json.loads(moralis_response.text).get("profileId")
        chain_id = json.loads(moralis_response.text).get("chainId")
        signature = request.signature

        user_data = UserCreateRequest(
            wallet_address=wallet_address,
            chain_id=chain_id,
            moralis_id=moralis_id,
        )

        user = await is_user_exist(user_data)
        if not user:
            try:
                user_profile = UserCreateRequest(
                    wallet_address=wallet_address,
                    chain_id=chain_id,
                    moralis_id=moralis_id,
                )

                user = await db_create_user(user_profile)
                if user:
                    logger.info(f"User created. Profile ID: {moralis_id}")
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
            moralis_id=moralis_id,
            wallet_address=wallet_address,
            signature=signature,
            chain_id=chain_id,
        )

        access_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES_ACCESS)
        access_token = create_access_token(
            jwt_user.model_dump(), expires_delta=access_token_expires
        )

        refresh_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES_REFRESH)
        refresh_token = create_refresh_token(
            jwt_user.model_dump(), expires_delta=refresh_token_expires
        )

        logger.info(f"User {wallet_address} authenticated. Profile ID: {user.id}")

        response_data = VerificationResponse(
            id=user.id,
            wallet_address=wallet_address,
            chain_id=chain_id,
            access_token=access_token,
            first_name=user.first_name,
            last_name=user.last_name,
            moralis_id=moralis_id,
        )

        # TODO: Consider storign refresh token inside a db
        await db_store_message(request.message, wallet_address)
        response.set_cookie(
            key=env.JWT_REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            max_age=env.JWT_EXPIRY_MINUTES_REFRESH * 60,
            samesite="none",
            secure=True,
        )

        return VerificationResponse(**response_data.model_dump())

    elif moralis_response.status_code == 400:
        logger.error(f"Challenge not found, Timeout may have exceeded.")
        raise HTTPException(
            status_code=400,
            detail=f"Challenge not found, Timeout may have exceeded",
        )

    else:
        logger.error(
            f"Verification failed. Could not authenticate user. {moralis_response.text}"
        )
        raise HTTPException(
            status_code=401,
            detail=f"Verification failed. Could not authenticate user. {moralis_response.text}",
        )


# Route: Generate JWT Token
# TODO: This not works as expected. Need to fix this
async def get_access_token(token_data: TokenDataRequest) -> TokenResponse:
    user = await authenticate_user(token_data)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES_ACCESS)
    access_token = create_access_token(
        data=token_data.model_dump(),
        expires_delta=access_token_expires,
    )

    refresh_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES_REFRESH)
    refresh_token = create_access_token(
        data=token_data.model_dump(),
        expires_delta=refresh_token_expires,
    )

    message = "Signable Message"
    await db_store_message(message, token_data.wallet_address)

    return TokenResponse(access_token=access_token, token_type="bearer")


# Route: GET Refresh Token
async def get_refresh_token(request: Request) -> TokenResponse:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        refresh_token = request.cookies.get(env.JWT_REFRESH_COOKIE_NAME)

        if refresh_token is None:
            raise credentials_exception
        # TODO: If consider to store the jwt refresh token in the database delete it from it.
        payload = jwt.decode(
            refresh_token, env.JWT_SECRET_REFRESH, algorithms=[env.JWT_ALGORITHM]
        )

        id = payload.get("id")
        moralis_id = payload.get("moralis_id")
        wallet_address = payload.get("wallet_address")
        signature = payload.get("signature")
        chain_id = payload.get("chain_id")

        if (
            moralis_id is None
            or wallet_address is None
            or signature is None
            or chain_id is None
            or id is None
        ):
            raise credentials_exception

        # Check if token has expired
        expiration_timestamp = payload.get("exp")
        if (
            expiration_timestamp is None
            or datetime.fromtimestamp(expiration_timestamp) < datetime.now()
        ):
            raise credentials_exception

        token_data = TokenDataRequest(
            id=id,
            moralis_id=moralis_id,
            signature=signature,
            chain_id=chain_id,
            wallet_address=wallet_address,
        )

    except JWTError:
        raise credentials_exception

    user = await auth.authenticate_user(token_data)
    if not user:
        raise credentials_exception

    access_token_expires = timedelta(minutes=env.JWT_EXPIRY_MINUTES_ACCESS)
    access_token = create_access_token(
        token_data.model_dump(), expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token, token_type="bearer")


async def logout(request: Request, response: Response) -> None:
    refresh_token = request.cookies.get(env.JWT_REFRESH_COOKIE_NAME)
    if refresh_token:
        try:
            # Decode the refresh token
            payload = jwt.decode(
                refresh_token, env.JWT_SECRET_REFRESH, algorithms=[env.JWT_ALGORITHM]
            )

            # Invalidate the token by setting expiration to now
            payload["exp"] = datetime.timestamp(datetime.now())

            # Optionally, clear the refresh token from cookies
            response.delete_cookie(
                env.JWT_REFRESH_COOKIE_NAME,
                httponly=True,
                samesite="none",
                secure=True,
            )

            await db_delete_stored_message(payload.get("wallet_address"))
            # Return a response indicating successful logout
            raise HTTPException(status_code=201, detail="Logged out successfully")

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=401,
            detail="Token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
