from app.utils.response import UserLoginResponse, UserRegisterResponse
from app.models.Users import User, ExistingUser
from app.utils.logging import setup_logger, get_logger
from app.utils.database import user_collection
from fastapi import HTTPException
from app.utils import jwt
from datetime import timedelta

setup_logger()
logger = get_logger()


# SECTION: FastAPI Login Routes -> Login
async def login(wallet_address: str, password: str) -> UserLoginResponse:
    user = user_collection.find_one({"wallet_address": wallet_address})
    if user:
        hashed_password = user["hash_password"]
        if jwt.pwd_context.verify(password, hashed_password):
            token_data = {"sub": str(user["_id"]), "wallet_address": wallet_address}
            access_token = jwt.create_access_token(data=token_data, expires_delta=timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES))
            
            return UserLoginResponse(
                code=200,
                response="User Login Successfull",
                data=ExistingUser(id=str(user["_id"]), access_token=access_token)
            )
        else:
            return UserLoginResponse(
                code=400,
                response="Incorrect Wallet address or Password",
                data=ExistingUser(id=None)
            )   
    else:
        return UserLoginResponse(
            code=404,
            response="User not found",
            data=ExistingUser(id=None)
        )
# SECTION: End of FastAPI Login Routes -> Login

# SECTION: FastAPI Auth Routes -> Registration
async def register(user_data: User) -> UserRegisterResponse:
    existing_user = user_collection.find_one({"wallet_address": user_data.wallet_address})
    if existing_user:
        return UserRegisterResponse(
            code=400,
            response="User already exists",
            data=ExistingUser(id=None)
        )
    
    hashed_password = jwt_handler.pwd_context.hash(user_data.hash_password)
    user_data.hash_password = hashed_password
    
    user_dict = user_data.dict()
    
    result = user_collection.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    return UserRegisterResponse(
            code=400,
            response="User Registered Successfully",
            data=ExistingUser(id=user_id)
        )
# SECTION: End of FastAPI Auth Routes -> Registration