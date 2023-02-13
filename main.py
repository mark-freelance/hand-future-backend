from fastapi import FastAPI

from packages.wechat.article import parse_wechat_article

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/wechat_article")
async def get_from_wechat_article(url: str):
    return parse_wechat_article(url)


