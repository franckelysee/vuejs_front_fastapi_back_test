from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, Header, Request, Response, Cookie, status
from fastapi.responses import JSONResponse
from App.Models.AuthCredentials.LoginCredentials import credentials
from sqlalchemy.orm import Session
from App.output_ports.db.Connexion import SessionLocal, get_db
from typing import Annotated, Dict, Optional
from App.Models.Models import User
from App.core.auth.UserAuth import AuthenticatedUser
from App.core.auth.LoginController import  ACCESS_TOKEN_EXPIRE_MINUTES,COOKIE_NAME, get_current_user_from_token 
from fastapi.security import OAuth2PasswordBearer
from App.inputs.schemas.UserSchema import UserSchema
from App.core.cases.authentication_use_case import AuthenticationUsecase 
from fastapi.encoders import jsonable_encoder


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")



router =  APIRouter(prefix='/auth', tags=['Handle account users'], include_in_schema=True)

@router.post("/token")
def login_for_access_token(response:Response,form_data:AuthenticatedUser):
  db = next(get_db())
  print("in the token")
  auth_usecase = AuthenticationUsecase(db=db)
  result = auth_usecase.login_access_token(form_data=form_data, response=response)
  print(result)
  if result:
    return result
    
      
@router.post("/login")
async def Login(response:Response, data:AuthenticatedUser):
  db = next(get_db())
  res = login_for_access_token(response,data)
  print("res",res)
  
  if res:
    res.update({"expired_at":ACCESS_TOKEN_EXPIRE_MINUTES})
    res.update({"cookie_name":COOKIE_NAME})
    
    #SETTING THE COOKIE
    max_age = res["expired_at"] *60
    response.set_cookie(COOKIE_NAME, res[COOKIE_NAME], path="/", max_age=max_age, samesite='None',secure=True)
    print()
  return jsonable_encoder(res)

@router.get("/user")
async def read_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
  current_user = get_current_user_from_token(token=token,db=db)
  print(current_user)
  return current_user