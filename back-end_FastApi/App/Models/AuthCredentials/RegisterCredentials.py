from pydantic import BaseModel

class R_credentials(BaseModel):
    username: str
    email: str
    password: str
    confirm_pass:str
    address: str