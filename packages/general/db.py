import pydantic
import pymongo
from bson import ObjectId

from env import ENV_MONGO_URI

# 它会在 fastapi 返回的时候被解析
# fix ObjectId & FastApi conflict, ref: https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = lambda x: {
    "id": str(x),
    # generation_time 是 datetime 类型，需要经过转换才可以输送给前端，调用 timestamp() 可以转成浮点数（"秒"为单位）
    "generation_time": x.generation_time.timestamp()
}

db_client = pymongo.MongoClient(ENV_MONGO_URI)
db = db_client["hand_future"]
coll_hero = db["hero"]
coll_user = db["user"]
coll_work = db['work']

if __name__ == '__main__':
    print(list(db['ld_products'].find()))
