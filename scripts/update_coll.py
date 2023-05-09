from src.libs.db import coll_user

for item in coll_user.find({"avatar": {"$ne": None}}):
    id = item['_id']
    avatar_name = item['avatar']
    coll_user.update_one({"_id": id}, {"$set": {"avatar": f"/files/{avatar_name}"}})
    print("updated ", id)
