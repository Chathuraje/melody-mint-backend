from fastapi import HTTPException, status

from app.api.v1.libraries.user.db import (
    db_create_user,
    db_delete_user,
    db_get_user_by_id,
    db_get_user_by_wallet_address,
    db_update_user,
)
from app.api.v1.utils.common import (
    is_user_exist,
    is_user_exist_by_id,
    is_valid_object_id,
    is_valid_support_chain,
    is_valid_wallet_address,
)
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.user import UserCreateRequest, UserUpdateRequest


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
async def get_user_by_wallet_address(address: str, chain_id: int) -> UserResponse:
    try:
        if not is_valid_support_chain(chain_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported chain ID provided.",
            )

        if not await is_valid_wallet_address(address, chain_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid wallet address provided.",
            )

        user = await db_get_user_by_wallet_address(address, chain_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with wallet address: {address} not found.",
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

        exisitng_user = await is_user_exist(
            user_data.wallet_address, user_data.chain_id
        )
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


async def update_user(user_id: str, user_data: UserUpdateRequest) -> UserResponse:

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
