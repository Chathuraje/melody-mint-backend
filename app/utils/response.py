from pydantic import BaseModel, root_validator, Field
from typing import Generic, Optional, TypeVar
import json
from app.models.Base import LogContent
from app.models.Users import User, UserReturn, UserReturnID, Token
from app.models.Campaigns import Campaigns, CampaignsReturn, CampaignsNew, InvestCampaign
from app.models.MusicIdentifier import Music, MusicNew
from app.models.Marketplace import CollectionNew, Collections, CollectionsReturn

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
class UserLoginResponse(StandardResponse[UserReturnID]):
    pass
# End of User Login Response Model

# Token Response Model (StandardResponse -> Data)
class TokenResponse(StandardResponse[Token]):
    pass
# End of Token Response Model


# User Register Response Model (StandardResponse -> Data)
class UserRegisterResponse(StandardResponse[UserReturnID]):
    pass
#End of User Register Response Model

# Individual User Response Model (StandardResponse -> Data)
class IndividualUserResponse(StandardResponse[User]):
    pass
# End of User Register Response Model

# All Users Response Model (StandardResponse -> Data)
class AllUsersResponse(StandardResponse[list[UserReturn]]):
    pass
# End of All Users Response Model



# Campaign Create Response Model (StandardResponse -> Data)
class CampaignCreateResponse(StandardResponse[CampaignsNew]):
    pass
#End of Campaign Create Response Model

# Single Campaign Response Model (StandardResponse -> Data)
class SingleCampaignResponse(StandardResponse[Campaigns]):
    pass
# End of Single Campaign Response Model

# All Campaigns Response Model (StandardResponse -> Data)
class AllCampaignResponse(StandardResponse[list[CampaignsReturn]]):
    pass
# End of All Campaigns Response Model


# Investment Response Model (StandardResponse -> Data)
class InvestmentResponse(StandardResponse[InvestCampaign]):
    pass
# End of Investment Response Model

# Music Music Train Response Model (StandardResponse -> Data)
class MusicTrainResponse(StandardResponse[MusicNew]):
    pass
# End of Music Train Response Model

# Music Identifier Response Model (StandardResponse -> Data)
class MusicIdentifierResponse(StandardResponse[Music]):
    pass
# End of Music Identifier Response Model


# Campaign Create Collection Model (StandardResponse -> Data)
class CollectionCreateResponse(StandardResponse[CollectionNew]):
    pass
#End of Campaign Create Response Model

# Single Campaign Response Model (StandardResponse -> Data)
class SingleCampaignResponse(StandardResponse[Collections]):
    pass
# End of Single Campaign Response Model

# All Collection Response Model (StandardResponse -> Data)
class AllCampaignResponse(StandardResponse[list[CollectionsReturn]]):
    pass
# End of All Collection Response Model