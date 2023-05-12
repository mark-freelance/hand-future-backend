import dotenv

from src.api.root import root_router
from src.config.rest import origins

dotenv.load_dotenv()

from fastapi import FastAPI
from starlette.middleware import Middleware

# 不要用这个，ref: https://github.com/tiangolo/fastapi/issues/1663#issuecomment-730089066
# from fastapi.middleware.cors import CORSMiddleware
# 要用这个：
from starlette.middleware.cors import CORSMiddleware

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
    ],
)

app.include_router(root_router)
