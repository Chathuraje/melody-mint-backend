from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.user import UserCreateRequest, UserUpdateRequest
from app.api.v1.libraries.auth.jwt import get_current_user
from app.utils import logging

from app.api.v1.libraries.user import user

user_router = APIRouter(prefix="/user", responses={404: {"description": "Not found"}})
logger = logging.getLogger()

user_dependency = Annotated[dict, Depends(get_current_user)]


@user_router.post(
    "/",
    description="Create User Profile",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: UserCreateRequest):
    logger.info("Create User Profile endpoint accessed")

    return await user.create_user(user_data)


@user_router.get(
    "/{user_id}",
    description="Get User Profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str):
    logger.info("Get User Profile endpoint accessed")

    return await user.get_user(user_id)


@user_router.put(
    "/{user_id}",
    description="Update User Profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(user_id: str, user_data: UserUpdateRequest):
    logger.info("Update User Profile endpoint accessed")
    return await user.update_user(user_id, user_data)


@user_router.delete(
    "/{user_id}",
    description="Delete User Profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: str):
    logger.info("Delete User Profile endpoint accessed")

    return await user.delete_user(user_id)


@user_router.get(
    "/wallet/{address}/{chain_id}",
    description="Get User Profile by Wallet Address",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_wallet_address(address: str, chain_id: int):
    logger.info("Get User Profile by Wallet Address endpoint accessed")

    return await user.get_user_by_wallet_address(address, chain_id)
