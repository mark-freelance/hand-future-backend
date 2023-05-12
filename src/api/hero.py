import json
import os
import time
from typing import List

from fastapi import APIRouter, Query
from notion_client import Client
from notion_client.helpers import collect_paginated_api
from pymongo import UpdateOne
from starlette.background import BackgroundTasks

from src.ds.graph import IGraphData
from src.ds.notion import NotionModel
from src.ds.user import HeroModel
from src.libs.db import coll_hero_notion, coll_user
from src.libs.env import NOTION_DATABASE_ID, NOTION_TOKEN
from src.libs.log import getLogger
from src.libs.path import CACHE_DIR

hero_router = APIRouter(prefix="/hero", tags=["hero"])

logger = getLogger("hero-api")

AVATAR_MAP = {}


@hero_router.get(
    '/',
    summary='heroes 是 users 的子集',
    response_model=List[HeroModel],
    response_model_by_alias=False,
)
async def list_heroes():
    return list(coll_user.find({"is_hero": True}))


@hero_router.post(
    "/init_from_notion",
    summary='todo: 该接口要限速',
)
async def init_heroes(
        bt: BackgroundTasks,
        use_dump_json: bool = False,
        use_dump_db: bool = True,
        fields: list[str] = Query(['id']),
) -> list[dict]:
    notion = Client(auth=NOTION_TOKEN)
    # full data, ref: https://github.com/ramnes/notion-sdk-py#utility-functions
    data = collect_paginated_api(notion.databases.query, database_id=NOTION_DATABASE_ID)

    logger.info(f"dumping {len(data)} records of heroes...")

    def dump_json():
        fp = os.path.join(CACHE_DIR, f'data-{time.time_ns()}.json')
        with open(fp, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'written into file://{fp}')

    def dump_db():
        coll_hero_notion_tasks = []
        coll_user_tasks = []
        for seq, item in enumerate(data):
            # pprint(item)
            id = item['id']
            coll_hero_notion_tasks.append(  # update raw data, in order to save a full mirror
                UpdateOne({"_id": id}, {"$set": dict(**item, _id=id)}, upsert=True))
            hero_model = NotionModel.parse_obj(item).to_hero_model(bt)
            coll_user_tasks.append(
                UpdateOne({"_id": id}, {"$set": dict(**hero_model.dict(exclude_unset=True), _id=id)}, upsert=True))
        result_hero_notion = coll_hero_notion.bulk_write(coll_hero_notion_tasks).bulk_api_result
        result_user = coll_user.bulk_write(coll_user_tasks).bulk_api_result
        logger.info({"result": {'hero_notion': result_hero_notion, 'user': result_user}})

    if use_dump_json: dump_json()

    if use_dump_db: dump_db()

    return [{key: item[key] for key in fields} for item in data]


@hero_router.get(
    '/graph_data',
    description='直接读取 user 表里是notion hero的用户，并筛选有头像的，进行携手链接'
)
async def get_graph_data():
    nodes = list(coll_user.find({"avatar": {"$ne": None}, "is_hero": True}))
    ids = [i['id'] for i in nodes]
    links = []
    seen = set()  # 要去重
    for node in nodes:
        source = node['id']
        if source in ids:
            for link in node['partners']:
                if link in ids:
                    target = link
                    cur = ",".join(sorted([source, target]))
                    if cur not in seen:
                        seen.add(cur)
                        links.append({"source": source, "target": target})

    graph_data: IGraphData = {"nodes": nodes, "links": links}
    # print(graph_data)
    return graph_data
