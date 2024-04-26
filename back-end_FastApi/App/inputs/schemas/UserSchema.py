from typing import Annotated, Optional
from pydantic import BaseModel



class UserSchema(BaseModel):
    id:Optional[int]
    username:Optional[str]
    email:Optional[str]
    
    class Config:
        orm_mode = True


class PasswordForm(BaseModel):
    password:str
    
class User(UserSchema):
    password:str