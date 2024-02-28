from fastapi import APIRouter, HTTPException
from app.utils.logging import setup_logger, get_logger
from app.api.auth.libraries import auth
from app.utils.response import UserRegisterResponse, UserLoginResponse
from app.models.Users import User

setup_logger()
logger = get_logger()

router = APIRouter()

@router.get("/login/{wallet_address}", response_model=UserLoginResponse)
async def login(wallet_address):
    logger.info("Login endpoint accessed.")
    
    return await auth.login(wallet_address)

@router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: User):
    logger.info("Register endpoint accessed.")
    return await auth.register(user_data)

# @router.get("/logout", response_model=StandardResponse)
# async def logout():
#     logger.info("Logout endpoint accessed.")
#     return await auth.logout()