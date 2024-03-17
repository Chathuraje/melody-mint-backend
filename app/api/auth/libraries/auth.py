from app.utils.response import UserLoginResponse, UserRegisterResponse, TokenResponse
from app.models.Users import UserReturnID, UserReturn, Token, ChallengeReqeust, ChallengeResponse, User
from app.utils.logging import setup_logger, get_logger
from app.utils.database import user_collection
from fastapi import HTTPException, Request
from app.utils.auth import jwt
from moralis import evm_api
from app.utils import config
import json
from datetime import datetime, timedelta, timezone
import requests

setup_logger()
logger = get_logger()


async def request_challenge(request: ChallengeReqeust):
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + 'Z'
    
    REQUEST_URL = f'https://authapi.moralis.io/challenge/request/{request.network}'
    request_object = {
      "domain": "defi.finance",
      "chainId": request.chainId,
      "address": request.address,
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": expirationTime,
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    response = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': config.MORALIS_API_KEY}
    )
    
    return json.loads(response.text)


async def verify_message(request: ChallengeResponse):
    
    request = request.dict()
    
    REQUEST_URL = f'https://authapi.moralis.io/challenge/verify/{request["network"]}'
    response = requests.post(
        REQUEST_URL,
        json=request,
        headers={'X-API-KEY': config.MORALIS_API_KEY})
    if response.status_code == 201: # user can authenticate
        eth_address=json.loads(response.text).get('address')
        logger.info(f"User {eth_address} authenticated")
        
        return  await login(eth_address)
    else:
        logger.info("User not authenticated")
        return UserLoginResponse(
            code=404,
            response="User not found",
            data=UserReturnID(id=None)
        ) 

# SECTION: FastAPI Login Routes -> Login
async def login(wallet_id) -> UserLoginResponse:
    user = user_collection.find_one({"wallet_address": wallet_id})
    if user is None:
        return UserLoginResponse(
            code=404,
            response="User not found",
            data=UserReturnID(id=None)
        )
    
    # user = jwt.authenticate_user(user_data.wallet_address, user_data.password)
    # if user:
    return UserLoginResponse(
        code=200,
        response="User Login Successfull",
        data=UserReturnID(id=str(user["_id"]))
    )
    # else:
    #     return UserLoginResponse(
    #         code=401,
    #         response="Invalid Password",
    #         data=UserReturnID(id=None)
    #     )
# SECTION: End of FastAPI Login Routes -> Login

# SECTION: FastAPI Auth Routes -> Registration
async def register(user_data: User) -> UserRegisterResponse:
    existing_user = user_collection.find_one({"wallet_address": user_data.wallet_address})
    if existing_user:
        return UserRegisterResponse(
            code=400,
            response="User already exists",
            data=None
        )
    
    # user_data.hash_password = jwt.get_password_hash(user_data.hash_password)
    user_dict = user_data.dict()
    
    result = user_collection.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    return UserRegisterResponse(
            code=200,
            response="User Registered Successfully",
            data=UserReturnID(id=user_id)
        )
# SECTION: End of FastAPI Auth Routes -> Registration

# SECTION: Access for Token Authentication
async def login_for_access_token(form_data) -> Token:
    user = user_collection.find_one({"wallet_address": form_data.username})
    if user is None:
        return TokenResponse(
            code=401,
            response="Invalid Username or Password",
            data=None
        )
    
    user = jwt.authenticate_user(form_data.username, form_data.password)
    if user:
        access_token_expires = jwt.ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = jwt.create_access_token(
            data={"sub": user["wallet_address"]},
            expires_delta=access_token_expires
        )
        return TokenResponse(
            code=200,
            response="Access Token Generated",
            data=Token(access_token=access_token, token_type="bearer")
        )
    else:
        return TokenResponse(
            code=401,
            response="Invalid Username or Password",
            data=None
        )
# SECTION: End of Access for Token Authentication