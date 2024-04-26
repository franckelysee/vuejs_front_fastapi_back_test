from sqlalchemy.orm import Session
from App.inputs.schemas.AuthenticationSchema import Token
from App.inputs.schemas.UserSchema import UserSchema
from App.core.auth.LoginController import ACCESS_TOKEN_EXPIRE_MINUTES, user_authenticated, create_access_token
from fastapi import Response, Request, HTTPException,status
from datetime import datetime, time, timedelta, timezone
from App.core.auth.UserAuth import AuthenticatedUser

class AuthenticationUsecase:
    def __init__(self, db:Session) -> None:
        self.db = db
        
    
    def login_access_token(self,form_data:AuthenticatedUser, response:Response)->Token:
        # if not user:
        #   response.status_code = status.HTTP_401_UNAUTHORIZED
        #   return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Password Incorrect")
        credentials_Exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
        user = user_authenticated(self.db,form_data.email, form_data.password)
        print(user)
        if not user:
            raise credentials_Exception
        
        
        acces_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        acces_token = create_access_token(
            data = {"tk_email": user.email},
            expire_delta=acces_token_expires
        )
        p_user = UserSchema(
            id=user.id,
            email=user.email
        )
        result = {"access_token":acces_token, "token_type":"bearer", "user":p_user}
        print("from token",user)
        
        return result