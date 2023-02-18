
import uvicorn
from fastapi import FastAPI

from api.files import files_router
from api.wechat import wechat_router
from api.user.router import user_router
from api.hero.router import hero_router
from fastapi.middleware.cors import CORSMiddleware

from api.works.router import works_router
from config import HOST, PORT, IS_DEV

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

app.include_router(user_router)
app.include_router(works_router)
app.include_router(hero_router)
app.include_router(wechat_router)
app.include_router(files_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT, reload=IS_DEV)
