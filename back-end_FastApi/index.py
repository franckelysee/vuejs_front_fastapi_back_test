from typing import List, Optional, Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Cookie, Depends, FastAPI, HTTPException, Header, Query, Path, status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, time, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWSError, jwt
from passlib.context import CryptContext
from jwt_handler import signJWT
from jwt_bearer import jwtBearer


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router =  APIRouter(prefix='/index', tags=['ALL testing '], include_in_schema=True)

# Query Parameters
fake_items_db = [
    {"item_name":"Foo"},
    {"item_name":"Bar"},
    {"item_name":"Baz"}
]

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    username:str |None = None
    
class User(BaseModel):
    username:str
    email:str |None = None
    full_name:str|None = None
    disabled:bool|None = None

class UserInDB(User):
    hashed_password:str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/index/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username:str, password:str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta:timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWSError:
        raise credentials_exception
    
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user:Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User") 
    return current_user


@router.post("/token")
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()])->Token:
    user = authenticate_user(fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or Password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    acces_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username}, expires_delta=acces_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
    
    
    
@router.get("/users/me")
async def read_users_me(current_user:Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/item/")
async def read_items(token:Annotated[User, Depends(get_current_active_user)]):
    return {"token":token}


@router.get("/items/{item_id}")
async def read_item(item_id:Annotated[int, Path(title="the Id of the item to get")], q:Annotated[List[str] | None, Query(alias="item-query")]=...):
    if q:
        return {"item_id":item_id,"q":q}
    return {"item_id":item_id}

@router.get("/item_/{item_id}")
async def read_item(item_id:str, needed:str, q:Annotated[str | None, Query(max_length=50)]=None, short:bool = False):
    item = {"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description":"this is an amazing item that has a long description"}
        )
    
    return item

# Request Body

class Item(BaseModel):
    name:str
    description:Optional[str | None]=Field(
        default=None, title="The description of the item"
    )
    price:float = Field(gt=0, description="the price must be greater than zero")
    tax:float | None = None
    tags: set[str] = set()
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

    
class User(BaseModel):
    username: str
    full_name: str | None = None

@router.get("/items_put/{item_id}")
async def getItem_put(item_id:Annotated[int, Path()], item:Annotated[Item, Body(embed=True)]=... ):
    
    result = {"item_id":item_id , **item.dict()}
    return result
    
    
@router.post("/Body_items")
async def create_item(item:Item, user:User):
    item_dict = {**item.dict(), **user.dict()}
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
        
    return item_dict

#the pattern parameter is for the regex
@router.put("/items/{item_id}")
async def update_item(
    item_id:int, 
    item:Annotated[Item, Body(
        embed=True, 
        examples=[
            {"name":"foo", 
             "description":"A Very nice Item", 
             "price":36.4,
             "tax":3.2
            }
        ]
    )], 
    q:Annotated[List[str] |None, Query(max_length=50, min_length=3, pattern="^fixed")]=...
    ):
    result = { "item_id":item_id, **item.dict()}
    if q:
        result.update({"q":q})
    return result


# @router.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Annotated[datetime | None, Body()] = None,
#     end_datetime: Annotated[datetime | None, Body()] = None,
#     repeat_at: Annotated[time | None, Body()] = None,
#     process_after: Annotated[timedelta | None, Body()] = None,
# ):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }



class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)
    
    class Config:
        schema_extra = {
            "post_demo":{
                "title":"some title about animals",
                "content": "some content about animals"
            }
        }
        
class UserSchema(BaseModel):
    fullname:str = Field(default=None)
    email: EmailStr = Field(default=None)
    password : str = Field(default= None)
    
    class Config:
        schema_extra =  {
            "user_schema":{
                "fullname":"my name",
                "email":"example@gmail.com",
                "password":"string"
            }
        }
    
    
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password : str = Field(default= None)
    
   
posts = [
    {
        "id":1,
        "title":"Penguins",
        "content":"Penguins are a group of aquatic flightless birds."
    },
    {
        "id":2,
        "title":"Tigers",
        "content":"Tigers are the largest living cat species and members of the genus Panthera."
    },
    {
        "id":3,
        "title":"Koalas",
        "content":"Koalas is arboreal herbivorous marsupial native to Australia."
    },
]

users = []


@router.get("/posts", tags=["posts"])
async def get_posts():
    return {"data":posts}


@router.get("/posts/{id}",tags=["posts"])
async def get_one_post(id:int):
    if id> len(posts):
        return {"error":"Post with this id does not exist!"}

    for post in posts:
        if post["id"] == id:
            return {"data":post}
        
@router.post("/posts",dependencies=[Depends(jwtBearer())],tags=["posts"])
async def add_post(post:PostSchema):
    post.id = len(posts) + 1
    
    posts.append(post.dict())
    
    return {
        "data":posts
    }

@router.put("/posts/{id}", tags=["posts"])
async def update_post(id:int, post:PostSchema):
    id = int(id)
    msg = ""
    if id> len(posts):
        return {"error":"Post with this id does not exist!"}
    
    for pos in posts :
        if pos["id"] == id:
            pos["title"] = post.title
            pos["content"] = post.content
            return {"data":pos}



@router.post("/user/signup", tags=["user"])
def user_signup(user:UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data:UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@router.post("/user/login",tags=["user"])
def user_login(user:UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return { "error":"Invalid login deetails"}