from typing import Dict

import pymongo
from fastapi import APIRouter

from api.hero.ds import HeroModel
from api.hero.notion import crawl_notion_heroes, parse_notion_heroes_info
from api.hero.utils import get_task_of_update_hero
from db import coll_hero

hero_router = APIRouter(prefix="/hero", tags=["hero"])


@hero_router.post("/update_basic")
def update_basic(data: HeroModel):
    return coll_hero.bulk_write(get_task_of_update_hero(data))


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
    data = parse_notion_heroes_info(raw_data)
    tasks = list(map(get_task_of_update_hero, data))
    result = coll_hero.bulk_write(tasks, ordered=False)
    return result.bulk_api_result
