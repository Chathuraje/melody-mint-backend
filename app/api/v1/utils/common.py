import re
from bson import ObjectId

from app.api.v1.libraries.user.db import (
    db_get_user_by_id,
    db_get_user_by_wallet_address,
)
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.user import UserCreateRequest
from app.config.file_handle import load_support_blocchain_data
from app.utils.web3 import web3_check_is_valid_address


def is_valid_object_id(id: str) -> bool:
    return ObjectId.is_valid(id)


async def is_valid_wallet_address(address: str, chain_id: int) -> bool:
    return await web3_check_is_valid_address(address, chain_id)


def is_valid_support_chain(chain_id: int) -> bool:
    data = load_support_blocchain_data()
    return str(chain_id) in data


async def is_user_exist(user_data: UserCreateRequest) -> UserResponse | None:
    # TODO: Check is the user data Already exists in the Blockchain using the hash of the user data
    # TODO: If exists cross check it with the db data to check mutability of the data
    
    user = await db_get_user_by_wallet_address(user_data)
    if user is not None:
        return UserResponse(**user.model_dump())


async def is_user_exist_by_id(id: str) -> UserResponse | None:
    user = await db_get_user_by_id(id)

    if user is None:
        return None
    return UserResponse(**user.model_dump())