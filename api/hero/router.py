import json
import os
from datetime import datetime
from typing import Dict, List

import pymongo
from fastapi import APIRouter

from api.hero.ds import HeroModel, NotionHeroModel
from api.hero.notion import crawl_notion_heroes, parse_notion_heroes_info
from db import coll_hero
from packages.general.session import session
from path import CACHE_DATA_DIR

hero_router = APIRouter(prefix="/heroes", tags=["heroes"])


@hero_router.patch("/update")
def update_basic(data: NotionHeroModel):
    return coll_hero.find_one_and_update(
        {"_id": data.id},
        {"$set": data.dict(exclude_unset=True)},
        return_document=True
    )


def get_task_of_update_hero(data: NotionHeroModel) -> pymongo.UpdateOne:
    """
    这个函数主要是用来照顾批量更新的

    :param data:
    :return:
    """
    res_avatar_notion = session.get(data.avatar_notion)
    res_file_upload = session.post('/files/upload', files={"file": (f"{data.name}.png", res_avatar_notion.content)})
    data.avatar = res_file_upload.json()['data']
    return pymongo.UpdateOne(
        {"id": data.id},
        {"$set": data.dict()},
        upsert=True
    )


@hero_router.get("/list")
def get_list() -> Dict:
    data = list(coll_hero.find({}, {}))
    return {
        "size": data.__len__(),
        "list": data
    }


@hero_router.get("/init")
def get_init_list() -> Dict:
    """
    todo: use raw (but should query the list)
    :return:
    """
    raw_data = crawl_notion_heroes()
    # 持久化方便复查
    with open(os.path.join(CACHE_DATA_DIR, f"notin_users_{datetime.now().isoformat()}.json"), "w") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    data: List[NotionHeroModel] = parse_notion_heroes_info(raw_data)
    tasks = list(map(get_task_of_update_hero, data))
    result = coll_hero.bulk_write(tasks, ordered=False)
    return result.bulk_api_result


@hero_router.put('/reset')
def reset():
    result = coll_hero.delete_many({})
    return result.raw_result
