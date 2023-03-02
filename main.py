import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware

# 不要用这个，ref: https://github.com/tiangolo/fastapi/issues/1663#issuecomment-730089066
# from fastapi.middleware.cors import CORSMiddleware
# 要用这个：
from starlette.middleware.cors import CORSMiddleware

from api.data import data_router
from api.files import files_router
from api.ld.router import ld_router
from api.wechat import wechat_router
from api.user.router import user_router
from api.hero.router import hero_router

from api.works.router import works_router
from config import HOST, PORT, IS_DEV

origins = [
    # "*" # 在开启 credentials 的情况下，不能用 *，否则会直接报错
    "http://localhost",
    "http://localhost:3000",

    "http://82.157.185.34",
    "http://82.157.185.34:3000",
    "https://82.157.185.34",
    "https://82.157.185.34:3000",

    "http://gkleifeng.com",
    "http://gkleifeng.com:3000",
    "https://gkleifeng.com",
    "https://gkleifeng.com:3000",

    'http://101.43.159.254',
    'http://101.43.159.254:3000',
    'https://101.43.159.254',
    'https://101.43.159.254:3000',

    # ld_admin project
    "http://localhost:3010",
    "http://82.157.185.34:3010",
    "http://gkleifeng.com:3010",
]

app = FastAPI(
    # ref: https://github.com/tiangolo/fastapi/issues/1663#issuecomment-738075572
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,  # 默认
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

app.include_router(user_router)
app.include_router(data_router)
app.include_router(works_router)
app.include_router(hero_router)
app.include_router(wechat_router)
app.include_router(files_router)
app.include_router(ld_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT, reload=IS_DEV)
