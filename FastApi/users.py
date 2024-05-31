from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


users_list = [User(id= 1, name= "dante", surname= "zarate", age= 31),
            User(id= 2,name= "cecilia", surname= "montejo", age= 31),
            User(id= 3, name= "aimee", surname= "solis", age= 30)]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "dante", "surname": "zarate", "age": 31},
            {"name": "cecilia", "surname": "montejo", "age": 31},
            {"name": "aimee", "surname": "solis", "age": 30}
            ]

@app.get("/users")
async def users():
    return users_list

@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
@app.get("/user/")
async def userquery(id: int):
    return search_user(id)

def search_user(id: int):
    users =  filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "no se ha encontrado el usuario solicitado"}
    
@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    users_list.append(user)
    return user

@app.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "no se ha actualizado el usuario"}
    return user

@app.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "no se ha eliminado el usuario"}