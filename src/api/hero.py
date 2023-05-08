import json
import os
import time
from typing import List, Set

from fastapi import APIRouter, Body, HTTPException, Query
from notion_client import Client
from notion_client.helpers import collect_paginated_api
from starlette import status

from src.config.notion import NOTION_DATABASE_ID
from src.ds.graph import IGraphLink, IGraphData
from src.libs.db import coll_heroes2, coll_hero, coll_hero_notion
from src.libs.log import getLogger
from src.libs.path import CACHE_DIR

hero_router = APIRouter(prefix="/hero", tags=["hero"])

logger = getLogger("API_Hero")

AVATAR_MAP = {}


@hero_router.get('/')
async def list_heroes():
    return list(coll_hero.find({}, {}))


@hero_router.get("/{id}")
async def get_hero(id: str):
    return coll_hero.find_one({"_id": id})


@hero_router.post("/")
async def init_heroes(
        use_dump_json=False,
        use_dump_db=True,
        fields: list[str] = Query(['id'])
) -> list[dict]:
    notion = Client(auth=os.environ["NOTION_TOKEN"])

    # full data
    # ref: https://github.com/ramnes/notion-sdk-py#utility-functions
    data = collect_paginated_api(notion.databases.query, database_id=NOTION_DATABASE_ID)

    def dump_json():
        fp = os.path.join(CACHE_DIR, f'data-{time.time_ns()}.json')
        with open(fp, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'written into file://{fp}')

    def dump_db():
        for seq, item in enumerate(data):
            id = item['id']
            coll_hero_notion.update_one({"_id": id}, {"$set": dict(**item, _id=id)}, upsert=True)
            print(f'updated seq={seq + 1}, id={id}')

    if use_dump_json: dump_json()

    if use_dump_db: dump_db()

    return [{key: item[key] for key in fields} for item in data]


@hero_router.patch("/update")
async def update_basic(data: dict = Body()):
    if not data.get('id'):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="hero id is required"
        )
    return coll_hero.find_one_and_update(
        {"_id": data['id']},
        {"$set": data},
        upsert=True,
        return_document=True
    )


@hero_router.put('/reset')
async def reset():
    result = coll_hero.delete_many({})
    return result.raw_result


@hero_router.get('/graph_data')
async def get_graph_data():
    for hero in get_hero():
        AVATAR_MAP[hero['id']] = hero['avatar']

    items = list(coll_heroes2.find(
        {"$expr": {"$gt": [{"$size": "$properties.照片.files"}, 0]}},
        {
            "_id": 0,
            "id": 1,
            # ref: https://stackoverflow.com/a/39196636/9422455
            "notion_avatar": {"$first": "$properties.照片.files.file.url"},
            "name": {"$first": "$properties.嘉宾姓名.title.plain_text"},
            "relations": "$properties.携手嘉宾.relation.id",
        }
    )
    )

    ids: Set[str] = set()
    nodes: List[dict] = []
    links: List[IGraphLink] = []
    for item in items:
        id = item['id']
        if id in AVATAR_MAP:
            item['avatar'] = AVATAR_MAP[id]
            ids.add(id)
            relations = item.pop("relations")
            nodes.append(item)
            for relation in relations:
                # links中的结点由于被筛选可能不存在
                if relation in ids:
                    links.append({"source": item['id'], "target": relation})

    graph_data: IGraphData = {
        "nodes": nodes,
        "links": links
    }
    # print(graph_data)
    return graph_data
