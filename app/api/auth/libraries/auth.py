from app.utils.response import UserLoginResponse, UserRegisterResponse
from app.models.Users import UserInDB, UserReturnID, UserReturn
from app.utils.logging import setup_logger, get_logger
from app.utils.database import user_collection
from fastapi import HTTPException


setup_logger()
logger = get_logger()


# SECTION: FastAPI Login Routes -> Login
async def login(user_data) -> UserLoginResponse:
    wallet_address = user_data.wallet_address
    password = user_data.password
    
    user = user_collection.find_one({"wallet_address": wallet_address})
    if user:
        if user.get("hash_password") != password:
            return UserLoginResponse(
                code=401,
                response="Invalid Wallet Address or Password",
                data=UserReturnID(id=None)
            )
        
        return UserLoginResponse(
            code=200,
            response="User Login Successfull",
            data=UserReturnID(id=str(user["_id"]))
            )
    else:
        return UserLoginResponse(
            code=404,
            response="User not found",
            data=UserReturnID(id=None)
        )
# SECTION: End of FastAPI Login Routes -> Login

# SECTION: FastAPI Auth Routes -> Registration
async def register(user_data: UserInDB) -> UserRegisterResponse:
    existing_user = user_collection.find_one({"wallet_address": user_data.wallet_address})
    if existing_user:
        return UserRegisterResponse(
            code=400,
            response="User already exists",
            data=None
        )
    
    user_dict = user_data.dict()
    
    result = user_collection.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    return UserRegisterResponse(
            code=200,
            response="User Registered Successfully",
            data=UserReturnID(id=user_id)
        )
# SECTION: End of FastAPI Auth Routes -> Registration