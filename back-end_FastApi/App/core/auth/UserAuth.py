from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from App.Models.Models import User
from fastapi import HTTPException, status, Response, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError





class AuthenticatedUser(BaseModel):
    email:str
    password:str
    
