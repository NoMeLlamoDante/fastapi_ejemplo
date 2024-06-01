from typing import Union
from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return "hola mundo"

@app.get("/url")
async def url():
    return { "url": "https://google.com"}

app.mount("/static",StaticFiles(directory="static"), name="static")