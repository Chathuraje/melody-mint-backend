import json
from time import sleep
from typing import Annotated
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.user import UserCreateRequest, UserUpdateRequest
from app.utils import logging
from app.api.v1.libraries.user import user

user_router = APIRouter(
    prefix="/users", tags=["Users"], responses={404: {"description": "Not found"}}
)
logger = logging.getLogger()

user_dependency = Annotated[UserResponse, Depends(user.get_profile)]


@user_router.get(
    "/profile",
    description="Get User Profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile(access_user: user_dependency):
    logger.info("Get User Profile endpoint accessed")
    return access_user


# TODO: NEED TO FIX THIS
@user_router.put(
    "/profile",
    description="Update User Profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    access_user: user_dependency,
    # user_data: UserUpdateRequest,
    user_data=Form(None),
    profile_hero: UploadFile = File(None),
    profile_image: UploadFile = File(None),
):
    logger.info("Update User Profile endpoint accessed")

    user_data = json.loads(user_data)
    user_data.pop("profile_hero", None)
    user_data.pop("profile_image", None)

    return await user.update_user(
        access_user.id, user_data, profile_hero, profile_image
    )


# @user_router.post(
#     "/wallet",
#     description="Get User Profile by Wallet Address",
#     response_model=UserResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_user_by_wallet_address(user_data: UserCreateRequest):
#     logger.info("Get User Profile by Wallet Address endpoint accessed")

#     return await user.get_user_by_wallet_address(user_data)


# @user_router.post(
#     "/",
#     description="Create User Profile",
#     response_model=UserResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_user(user_data: UserCreateRequest):
#     logger.info("Create User Profile endpoint accessed")

#     return await user.create_user(user_data)


# @user_router.get(
#     "/{user_id}",
#     description="Get User Profile",
#     response_model=UserResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_user(user_id: str):
#     logger.info("Get User Profile endpoint accessed")

#     return await user.get_user(user_id)


# @user_router.delete(
#     "/{user_id}",
#     description="Delete User Profile",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_user(user_id: str):
#     logger.info("Delete User Profile endpoint accessed")

#     return await user.delete_user(user_id)
