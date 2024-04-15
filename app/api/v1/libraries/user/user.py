from typing import Annotated
from fastapi import Depends, HTTPException, UploadFile, status

from app.api.v1.libraries.user.db import (
    db_create_user,
    db_delete_user,
    db_get_user_by_id,
    db_get_user_by_wallet_address,
    db_update_user,
)
from app.api.v1.schemas.auth import TokenDataRequest
from app.api.v1.utils.common import (
    is_user_exist,
    is_user_exist_by_id,
    is_valid_object_id,
    is_valid_support_chain,
    is_valid_wallet_address,
)
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.user import UserCreateRequest, UserUpdateRequest
from app.config import settings
from app.utils import auth
from jose import JWTError, jwt
from datetime import datetime
from fastapi import security

from app.utils.resources_handle import upload_image

env = settings.get_settings()
oauth2_bearer = security.OAuth2PasswordBearer(tokenUrl="/v1/auth/token")


# Route: Get User Profile
async def get_user(user_id: str) -> UserResponse:
    try:
        if not is_valid_object_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid ID, ID must be a valid ObjectId.",
            )

        user = await db_get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID: {user_id} not found.",
            )

        return user
    except Exception as e:
        raise e


# Route: Get User Profile by Wallet Address
async def get_user_by_wallet_address(user_data: UserCreateRequest) -> UserResponse:
    try:
        if not is_valid_support_chain(user_data.chain_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported chain ID provided.",
            )

        if not await is_valid_wallet_address(
            user_data.wallet_address, user_data.chain_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid wallet address provided.",
            )

        user = await db_get_user_by_wallet_address(user_data)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with wallet address: {user_data.wallet_address} not found.",
            )
        return user
    except Exception as e:
        raise e


# Route: Create User Profile
async def create_user(user_data: UserCreateRequest) -> UserResponse:
    try:
        if not is_valid_support_chain(user_data.chain_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported chain ID provided.",
            )

        if not await is_valid_wallet_address(
            user_data.wallet_address, user_data.chain_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid wallet address provided.",
            )

        exisitng_user = await is_user_exist(user_data)
        if exisitng_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with wallet address and chain ID already exists",
            )

        user = await db_create_user(user_data)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user.",
            )

        return user
    except Exception as e:
        raise e


async def update_user(
    user_id: str,
    user_data,
    profile_hero: UploadFile,
    profile_image: UploadFile,
) -> UserResponse:

    user_data = UserUpdateRequest(**user_data)

    if not is_valid_object_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID, ID must be a valid ObjectId.",
        )

    exisitng_user = await is_user_exist_by_id(user_id)
    if not exisitng_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID: {user_id} not found.",
        )

    # user_data = UserUpdateRequest(**user_data.model_dump())

    if profile_hero is not None:
        profile_hero_url = await upload_image("hero", user_id, profile_hero)
        user_data.profile_hero = profile_hero_url

    if profile_image is not None:
        profile_image_url = await upload_image("profile", user_id, profile_image)
        user_data.profile_image = profile_image_url

    return await db_update_user(user_id, user_data)


async def delete_user(user_id):
    if not is_valid_object_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID, ID must be a valid ObjectId.",
        )

    exisitng_user = await is_user_exist_by_id(user_id)
    if exisitng_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID: {user_id} not found.",
        )

    return await db_delete_user(user_id)


# Route: Get User Profile
async def get_profile(token: Annotated[str, Depends(oauth2_bearer)]) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, env.JWT_SECRET_ACCESS, algorithms=[env.JWT_ALGORITHM]
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

    return user
