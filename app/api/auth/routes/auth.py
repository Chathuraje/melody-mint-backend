from fastapi import APIRouter, HTTPException
from app.utils.logging import setup_logger, get_logger
from app.api.auth.libraries import auth
from app.utils.response import UserRegisterResponse, UserLoginResponse
from app.models.Users import User

setup_logger()
logger = get_logger()

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse)
async def login(wallet_address: str, password: str):
    logger.info("Login endpoint accessed.")
    
    return await auth.login(wallet_address, password)

@router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: User):
    logger.info("Register endpoint accessed.")
    return await auth.register(user_data)