from app.utils.response import IndividualUserResponse, AllUsersResponse
from app.models.Users import User, UserReturn
from app.utils.database import user_collection
from bson import ObjectId

# SECTION: FastAPI Individual User Routes -> Login
async def get_user(user_id: str) -> IndividualUserResponse:
    user_id_obj = ObjectId(user_id)
    
    user = user_collection.find_one({"_id": user_id_obj})
    if user:
        return IndividualUserResponse(
            code=200,
            response="User found",
            data=User(
                wallet_address=user.get("wallet_address"),
                username=user.get("username"),
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                email=user.get("email"),
                contact_no=user.get("contact_no"),
                country=user.get("country"),
                state=user.get("state"),
                profile_picture=user.get("profile_picture"),
                is_artist=user.get("is_artist"),
                artist_data=user.get("artist_data"),
                disabled=user.get("disabled"),
                id=user_id_obj
            )
        )
    else:
        return IndividualUserResponse(
            code=404,
            response="User not found",
            data=None
        )
# SECTION: End of FastAPI Individual User Routes -> Login


# SECTION FastAPI All Users List
async def get_all_users() -> AllUsersResponse:
    users = user_collection.find()
    individual_user_responses = []
    for user_data in users:
        user_id = str(user_data['_id'])
        user = UserReturn(
            wallet_address=user_data.get("wallet_address"),
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            email=user_data.get("email"),
            contact_no=user_data.get("contact_no"),
            country=user_data.get("country"),
            state=user_data.get("state"),
            profile_picture=user_data.get("profile_picture"),
            is_artist=user_data.get("is_artist"),
            artist_data=user_data.get("artist_data"),
            disabled=user_data.get("disabled"),
            id=user_id
        )
        individual_user_responses.append(user)

    # Create AllUsersResponse
    return AllUsersResponse(
        code=200,
        response=f"{len(individual_user_responses)} Users found",
        data=individual_user_responses
    )
# SECTION: End of FastAPI All Users List


# SECTION: FastAPI Individual User Routes -> Update
async def update_user(user_id: str, user: User) -> IndividualUserResponse:
    user_id_obj = ObjectId(user_id)
    user_data = user.dict()
    result = user_collection.update_one({"_id": user_id_obj}, {"$set": user_data})
    
    if result.modified_count > 0:
        return IndividualUserResponse(
            code=200,
            response="User updated successfully",
            data=user
        )
    else:
        return IndividualUserResponse(
            code=404,
            response="User not updated",
            data=None
        )
# SECTION: End of FastAPI Individual User Routes -> Update


# # SECTION: RastAPI Wallet Routes -> Wallet Amount
# async def get_wallet_amount(user_id):
#     user_id_obj = ObjectId(user_id)
#     user = user_collection.find_one({"_id": user_id_obj})
#     if user:
#         return basic.get_wallet_amount(user.get("wallet_address"))
#     else:
#         return None
# # SECTION: End of FastAPI Wallet Routes -> Wallet Amount