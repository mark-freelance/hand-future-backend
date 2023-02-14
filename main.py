import os.path

from fastapi import FastAPI, UploadFile

from api.files import files_router
from api.hero import hero_router
from api.wechat import wechat_router
from packages.wechat.article import parse_wechat_article
from fastapi.middleware.cors import CORSMiddleware
import uuid

from path import UPLOADED_DATA_DIR

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",

    "http://82.157.185.34",
    "http://82.157.185.34:3000",

    "http://gkleifeng.com",
    "http://gkleifeng.com:3000",

    "https://gkleifeng.com",
    "https://gkleifeng.com:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hero_router)
app.include_router(wechat_router)
app.include_router(files_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
