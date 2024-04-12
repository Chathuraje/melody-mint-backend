from typing import Annotated
from bson import ObjectId
from pydantic import BeforeValidator, Field
from app.api.v1.model.User import User

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserResponse(User):
    id: PyObjectId = Field(..., description="User ID")
