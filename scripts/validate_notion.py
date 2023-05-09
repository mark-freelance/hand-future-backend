import json
import os.path

from src.ds.notion import NotionModel
from src.libs.path import CACHE_DIR

fp = os.path.join(CACHE_DIR, 'data-1683604631965434000.json')

names_set = set()


def validate(item):
    # pprint(item)
    notion_model = NotionModel(**item)
    user_model = notion_model.to_hero_model(bt=None)
    user_name = user_model.name
    assert user_name not in names_set, f'重复（name={user_name})'
    names_set.add(user_name)


with open(fp, 'r') as f:
    users = json.load(f)

    for item in users:
        try:
            validate(item)
        except Exception as e:
            print(item['id'])
            print(e)
