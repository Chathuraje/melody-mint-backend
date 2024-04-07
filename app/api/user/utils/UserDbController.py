from app.model.User import UserResponse, UserProfile, UserCreateResponse
from app.utils.database import get_collection
from pymongo.errors import PyMongoError
from bson import ObjectId


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


async def create_user(user: UserProfile) -> UserCreateResponse | None:
    try:
        userCollection = await get_collection("users")
        data = await userCollection.insert_one(user.model_dump())

        if data.inserted_id:
            return UserCreateResponse(id=data.inserted_id)
        else:
            return None
    except PyMongoError:
        return None
