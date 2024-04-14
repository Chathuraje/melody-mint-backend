from app.api.v1.model.User import User
from app.utils import logging
from bson import ObjectId
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.user import UserCreateRequest, UserUpdateRequest
from app.config.database import get_collection
from pymongo.errors import PyMongoError
from app.config import settings
from app.utils.app_security import decrypt_message, encrypt_text

logger = logging.getLogger()
env = settings.get_settings()


async def db_get_user_by_id(id: str) -> UserResponse | None:
    try:
        user_collection = await get_collection("users")
        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user is not None:
            return UserResponse(id=user["_id"], **user)
        else:
            return None

    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


async def db_get_user_by_wallet_address(
    user_data: UserCreateRequest,
) -> UserResponse | None:
    try:
        user_collection = await get_collection("users")
        user = await user_collection.find_one(
            {
                "wallet_address": user_data.wallet_address,
                "chain_id": user_data.chain_id,
                "moralis_id": user_data.moralis_id,
            }
        )

        if user is not None:
            return UserResponse(id=user["_id"], **user)
        else:
            return None

    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


async def db_create_user(user_data: UserCreateRequest) -> UserResponse:

    try:
        user_collection = await get_collection("users")

        user = User(**user_data.model_dump())
        data = await user_collection.insert_one(user.model_dump())

        if data.inserted_id is not None:
            return UserResponse(id=data.inserted_id, **user_data.model_dump())
        else:
            raise Exception("Failed to create user")

    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


async def db_update_user(id: str, user: UserUpdateRequest) -> UserResponse:
    try:
        userCollection = await get_collection("users")
        data = await userCollection.update_one(
            {"_id": ObjectId(id)}, {"$set": user.model_dump()}
        )

        if data.modified_count > 0:
            return UserResponse(id=id, **user.model_dump())
        else:
            raise Exception("Failed to update user")
    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


async def db_delete_user(id: str) -> bool:
    try:
        userCollection = await get_collection("users")
        data = await userCollection.delete_one({"_id": ObjectId(id)})

        if data.deleted_count > 0:
            return True
        else:
            raise Exception("Failed to delete user")
    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


async def db_store_message(message: str, wallet_address: str) -> bool:
    try:
        user_collection = await get_collection("authentication")
        existing_doc = await user_collection.find_one(
            {"wallet_address": wallet_address}
        )
        new_message = encrypt_text(message)

        if existing_doc:
            completed = await user_collection.update_one(
                {"wallet_address": wallet_address}, {"$set": {"message": new_message}}
            )

            if completed.modified_count < 0:
                raise Exception("Failed to store message")
        else:
            completed = await user_collection.insert_one(
                {"wallet_address": wallet_address, "message": new_message}
            )

            if completed.inserted_id is None:
                raise Exception("Failed to store message")

        return True

    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


async def db_get_stored_message(wallet_address) -> str | None:
    try:
        user_collection = await get_collection("authentication")
        existing_doc = await user_collection.find_one(
            {"wallet_address": wallet_address}
        )

        if existing_doc:
            return decrypt_message(existing_doc["message"])
        else:
            return None

    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")




async def db_delete_stored_message(wallet_address) -> bool:
    try:
        user_collection = await get_collection("authentication")
        existing_doc = await user_collection.find_one(
            {"wallet_address": wallet_address}
        )

        if existing_doc:
            completed = await user_collection.delete_one(
                {"wallet_address": wallet_address}
            )

            if completed.deleted_count > 0:
                return True
            else:
                raise Exception("Failed to delete message")
        else:
            return True

    except PyMongoError as e:
        raise Exception(f"MongoDB error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")