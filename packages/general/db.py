import pydantic
import pymongo
from bson import ObjectId

from config import MONGO_URI

# fix ObjectId & FastApi conflict, ref: https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

db_client = pymongo.MongoClient(MONGO_URI)
db = db_client["hand_future"]
coll_hero = db["hero"]
coll_user = db["user"]
coll_work = db['work']
