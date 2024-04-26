from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, Header, Request, Response, Cookie, status
from fastapi.responses import JSONResponse
from App.Models.AuthCredentials.RegisterCredentials import R_credentials
from sqlalchemy.orm import Session
from App.output_ports.db.Connexion import SessionLocal
from App.Models.Models import User
import json
from regex import *


router =  APIRouter(prefix='', tags=['Register ROute'], include_in_schema=False)


def get_db():
    db = SessionLocal()
    try:
      yield db
    except:
      print('Something went wrong')
    finally:
      db.close()


@router.post("/register")
async def register_user(request:Request, response:Response, db:Session=Depends(get_db)):
  form_data = json.loads(await request.body())
  # form_data = await request.body()
  
  user = db.query(User).filter(User.email == form_data["email"]).first()
  
  if user:
    response.status_code = status.HTTP_409_CONFLICT
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exists")
  else:
    print("He is new")
  
  
  
  print(form_data)