import pydantic
import pymongo
from bson import ObjectId

from src.libs.env import DATABASE_MONGO_URI, DATABASE_DB_NAME

# 它会在 fastapi 返回的时候被解析
# fix ObjectId & FastApi conflict, ref: https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = lambda x: {
    "id": str(x),
    # generation_time 是 datetime 类型，需要经过转换才可以输送给前端，调用 timestamp() 可以转成浮点数（"秒"为单位）
    "generation_time": x.generation_time.timestamp()
}

db_client = pymongo.MongoClient(DATABASE_MONGO_URI)

db = db_client[DATABASE_DB_NAME]
db_client = pymongo.MongoClient(DATABASE_MONGO_URI)
coll_hero = db["hero"]
coll_hero_notion = db["hero_notion"]
coll_hero_user = db['hero_user']
coll_user = db["user"]
coll_work = db['work']
