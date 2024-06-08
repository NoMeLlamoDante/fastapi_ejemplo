from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client
from bson.objectid import ObjectId

from pprint import pprint

router = APIRouter(prefix="/usersdb", 
                    tags=["usersdb"], 
                    responses={status.HTTP_404_NOT_FOUND:{"message":"no encontrado"}})

users_list = []

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
@router.get("/user/")
async def userquery(id: int):
    return search_user(id)

def search_user(id: int):
    users =  filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "no se ha encontrado el usuario solicitado"}

@router.get("/")
async def users():
    return users_list
    
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # if type(search_user(user.id)) == User:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="El usuario ya existe")
    # users_list.append(user)
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id":id}))
    return User(**new_user)

@router.put("/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "no se ha actualizado el usuario"}
    return user

@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "no se ha eliminado el usuario"}