from datetime import datetime, timedelta,timezone
from typing import Annotated, Union

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
SECRET = "a1acf3f9da84da9f289e5dd6cd5259bb"

router = APIRouter()

users_db = {
    "dante" : {
        "username": "dante",
        "full_name": "Dante Doe",
        "email": "example@gmail.com",
        "password": "$2a$12$QfIBPQY1cyXcLUJKyyxEeeyIfIpFlh2nHWPM0qmgIUc28i4U7KamW",
        "disabled": False,
    },
    "dante2":{
        "username": "dante2",
        "full_name": "Dante2 doe",
        "email": "example2@gmail.com",
        "password": "$2a$12$..uICYaa3DuyciHZe5FJo.vdXNoSuhcYyGJqo3WyyHCZK9NCwBpui",
        "disabled": True,
    },
}

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#bcrypt 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    full_name : str
    email: str
    disabled: bool

class UserDB(User):
    password: str

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="no autorizado", 
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        decode = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        print(dict(decode))
        username = decode.get("sub")
        if username is None:
            raise exception
        
    except Exception as e:
        print(e)
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto", headers={"WWW-Authenticate": "Bearer"})
    user = search_user_db(form.username)
    if not pwd_context.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    access_token = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),

    }
    return {"access_token": jwt.encode(access_token,SECRET,ALGORITHM), "token_type":"JWT"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user