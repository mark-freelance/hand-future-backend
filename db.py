import pydantic
import pymongo
from bson import ObjectId

# fix ObjectId & FastApi conflict, ref: https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

MONGO_URI = "mongodb://admin:admin@82.157.185.34:2099"

db_client = pymongo.MongoClient(MONGO_URI)
db = db_client["hand_future"]
coll_hero = db["hero"]
