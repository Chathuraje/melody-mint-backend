from fastapi import APIRouter, HTTPException, Depends
from app.utils.logging import get_logger
from app.api.users.libraries import users
from app.utils.response import IndividualUserResponse, AllUsersResponse
from app.models.Users import User
from app.utils.auth.auth import get_current_active_user

router = APIRouter()
logger = get_logger()

# @router.get("/", response_model=AllUsersResponse)
# async def get_all_users(current_user: User = Depends(get_current_active_user)):
#     logger.info("Getting all users")
#     return await users.get_all_users()

@router.get("/", response_model=AllUsersResponse)
async def get_all_users():
    logger.info("Getting all users")
    return await users.get_all_users()

@router.get("/{user_id}", response_model=IndividualUserResponse)
async def get_user(user_id: str):
    logger.info(f"Getting user profile with ID: {user_id}")
    user = await users.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=IndividualUserResponse)
async def update_user(user_id: str, user: User):
    logger.info(f"Updating user profile with ID: {user_id}")
    updated_user = await users.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

