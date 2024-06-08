from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name : str
    email: str
    disabled: bool

users_db = {
    "dante" : {
        "username": "dante",
        "full_name": "Dante Doe",
        "email": "example@gmail.com",
        "password": "123456",
        "disabled": False,
    },
    "dante2":{
        "username": "dante2",
        "full_name": "Dante2 doe",
        "email": "example2@gmail.com",
        "password": "654321",
        "disabled": True,
    },
}


class UserDB(User):
    password: str


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="no autorizado", 
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto", headers={"WWW-Authenticate": "Bearer"})
    user = search_user_db(form.username)
    if form.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    return {"access_token": user.username, "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user