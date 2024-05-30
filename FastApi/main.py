from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "hola mundo"

@app.get("/url")
async def url():
    return { "url": "https://google.com"}

