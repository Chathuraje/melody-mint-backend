from fastapi import APIRouter, HTTPException, Depends
from app.utils.logging import setup_logger, get_logger
from app.api.auth.libraries import auth
from app.utils.response import UserRegisterResponse, UserLoginResponse, TokenResponse
from app.models.Users import UserInDB, UserLogin, Token
from fastapi.security import OAuth2PasswordRequestForm

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

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("Login for access token")
    return await auth.login_for_access_token(form_data)
    