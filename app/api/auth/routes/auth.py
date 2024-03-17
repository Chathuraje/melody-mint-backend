from fastapi import APIRouter, HTTPException, Depends, Request
from app.utils.logging import setup_logger, get_logger
from app.api.auth.libraries import auth
from app.utils.response import UserRegisterResponse, UserLoginResponse, TokenResponse
from app.models.Users import UserLogin, Token, ChallengeReqeust, ChallengeResponse, User
# from fastapi.security import OAuth2PasswordRequestForm
import moralis

setup_logger()
logger = get_logger()

router = APIRouter()

@router.post("/login/{wallet_id}", response_model=UserLoginResponse)
async def login(wallet_id):
    logger.info("Login endpoint accessed.")
    return await auth.login(wallet_id)

@router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: User):
    logger.info("Register endpoint accessed.")
    return await auth.register(user_data)

# @router.post("/token", response_model=TokenResponse)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     logger.info("Login for access token")
#     return await auth.login_for_access_token(form_data)
    
@router.post("/request_challenge")
async def request_challenge(request: ChallengeReqeust):
    logger.info("Request message endpoint accessed.")
    return await auth.request_challenge(request)


@router.post("/verify_challenge")
async def verify_message(request: ChallengeResponse):
    logger.info("Verify message endpoint accessed.")
    return await auth.verify_message(request)