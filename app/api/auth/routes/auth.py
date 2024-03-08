from fastapi import APIRouter, HTTPException
from app.utils.logging import setup_logger, get_logger
from app.api.auth.libraries import auth
from app.utils.response import UserRegisterResponse, UserLoginResponse
from app.models.Users import UserInDB, UserLogin

setup_logger()
logger = get_logger()

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse)
async def login(user_data: UserLogin):
    logger.info("Login endpoint accessed.")
    
    return await auth.login(user_data)

@router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: UserInDB):
    logger.info("Register endpoint accessed.")
    return await auth.register(user_data)