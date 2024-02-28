from pydantic import BaseModel, root_validator, Field
from typing import Generic, Optional, TypeVar
import json
from app.models.Base import LogContent
from app.models.Users import ExistingUser

# Standard Response Model (Code, Response, Data)
T = TypeVar('T')

def get_error_message(code: int) -> str:
    try:
        with open("app/config/errors.json", "r") as file:
            error_codes = json.load(file)
        return error_codes.get(str(code), "Unknown error")
    except Exception as e:
        return "Unknown error"
class StandardResponse(BaseModel, Generic[T]):
    code: int = Field(..., description="Status code of the response")
    response: Optional[str] = Field(None, description="Message accompanying the status code")
    data: Optional[T] = Field(None, description="Content of the response")

    @root_validator(pre=True)
    def set_default_message(cls, values):
        code, message = values.get('code'), values.get('response')
        if message is None and code is not None:
            values['response'] = get_error_message(code)
        return values
# End of Standard Response Model

  
# Read Log Response Model (StandardResponse -> Data)
class ReadLogResponse(StandardResponse[LogContent]):
    pass
# End of Log Response Model


# User Login Response Model (StandardResponse -> Data)
class UserLoginResponse(StandardResponse[ExistingUser]):
    pass
# User End of User Login Response Model


# User Register Response Model (StandardResponse -> Data)
class UserRegisterResponse(StandardResponse[ExistingUser]):
    pass
# User End of Register Response Model