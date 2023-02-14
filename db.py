import pymongo

MONGO_URI = "mongodb://admin:admin@82.157.185.34:2099"

db_client = pymongo.MongoClient(MONGO_URI)
db = db_client["hand_future"]
coll_hero = db["hero"]
