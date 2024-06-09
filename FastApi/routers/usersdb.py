from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

from pprint import pprint

router = APIRouter(prefix="/usersdb", 
                    tags=["usersdb"], 
                    responses={status.HTTP_404_NOT_FOUND:{"message":"no encontrado"}})

users_list = []

@router.get("/{id}") #Path
async def user(id: str):
    return search_user(field="_id",key=ObjectId(id))
    
@router.get("/user/") #Query
async def userquery(email: str):
    print(email)
    return search_user(field="email", key=email)

def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "no se ha encontrado el usuario"}

@router.get("/", response_model=list[User])
async def users():
    print("entra")
    return users_schema(db_client.local.users.find())
    
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user(field="email", key=user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="El usuario ya existe")
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id":ObjectId(id)}))
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

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No eliminado")
    