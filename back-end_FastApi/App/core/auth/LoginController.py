from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import time, datetime, timedelta, timezone
from decouple import config
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.core.auth.UserAuth import AuthenticatedUser
from App.Models.Models import User
from App.inputs.schemas.UserSchema import UserSchema
from App.inputs.schemas.AuthenticationSchema import TokenData

SECRET = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
COOKIE_NAME = config("COOKIE_NAME")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")





def get_user(db:Session,email):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    
    
def user_authenticated(db:Session,email, password):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False
    if not user.password == password:
        return False
    return user
            
     

def create_access_token(data:dict, expire_delta:timedelta|None= None):
    to_encode=data.copy()
    
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, key=SECRET, algorithm=ALGORITHM)
    return encode_jwt


def decode_token(token:str, db: Session):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
            
    try:
        payload = jwt.decode(token=token, key=SECRET, algorithms=[ALGORITHM])
        email:str = payload.get("tk_email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user(db=db,email=token_data.email)
    
    if user is None:
        raise credentials_exception
    
    return user


def get_current_user_from_token(token:Annotated[str, Depends(oauth2_scheme)], db:Session)->UserSchema:
    print(token)

    user = decode_token(token,db=db)
    return user  