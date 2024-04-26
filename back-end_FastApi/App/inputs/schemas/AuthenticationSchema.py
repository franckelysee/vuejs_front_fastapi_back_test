from pydantic import BaseModel
from App.inputs.schemas.UserSchema import UserSchema


class Token(BaseModel):
    access_token: str
    token_type: str
    user:UserSchema
    
    
class TokenData:
    email:str |None = None