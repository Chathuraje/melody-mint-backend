from bson import ObjectId
from app.model.User import UserResponse, UserProfile
from app.utils.database import get_collection
from pymongo.errors import PyMongoError


async def get_user_by_wallet_address(
    address: str, chain_id: int
) -> UserResponse | None:
    try:
        userCollection = await get_collection("users")
        user = await userCollection.find_one(
            {"wallet_address": address, "chain_id": chain_id}
        )

        if user is not None:
            return UserResponse(id=user["_id"], **user)
        else:
            return None
    except PyMongoError:
        return None


async def create_user(user: UserProfile) -> UserResponse | None:
    try:
        userCollection = await get_collection("users")
        data = await userCollection.insert_one(user.model_dump())

        if data.inserted_id:
            return UserResponse(id=data.inserted_id, **user.model_dump())
        else:
            return None
    except PyMongoError:
        return None


async def get_user_by_id(id: str) -> UserResponse | None:
    try:
        userCollection = await get_collection("users")
        user = await userCollection.find_one({"_id": ObjectId(id)})

        if user is not None:
            return UserResponse(id=user["_id"], **user)
        else:
            return None
    except PyMongoError:
        return None
