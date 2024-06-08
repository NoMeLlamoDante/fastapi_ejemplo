from typing import Union
from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users,usersdb
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(usersdb.router)

@app.get("/")
async def root():
    return "hola mundo"

@app.get("/url")
async def url():
    return { "url": "https://google.com"}

app.mount("/static",StaticFiles(directory="static"), name="static")