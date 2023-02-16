import pymongo

from api.hero.ds import HeroModel


def get_task_of_update_hero(data: HeroModel) -> pymongo.UpdateOne:
    return pymongo.UpdateOne(
        {"id": data.id},
        {"$set": data.dict()},
        upsert=True
    )
