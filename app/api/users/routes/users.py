from fastapi import APIRouter
from app.utils.logging import setup_logger, get_logger
from app.api.users.libraries import users
from app.utils.response import IndividualUserResponse, AllUsersResponse
from app.models.Users import User

setup_logger()
logger = get_logger()

router = APIRouter()

@router.get("/", response_model=AllUsersResponse)
async def get_all_users():
    logger.info("Getting all users")
    return await users.get_all_users()

@router.get("/{user_id}", response_model=IndividualUserResponse)
async def get_user(user_id: str):
    logger.info("Getting user profile with ID: {user_id}")
    
    return await users.get_user(user_id)