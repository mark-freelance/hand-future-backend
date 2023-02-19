import json
import os.path
from pprint import pprint
from typing import List
from unittest import TestCase

from api.hero.ds import NotionHeroModel
from api.hero.notion import get_notion_avatar_url
from config import NOTION_COL_MAP
from packages.general.re import parse_p1
from path import CACHE_DATA_DIR


class Test(TestCase):
    def test_parse_notion_heroes_info(self):
        # self.fail()
        latest_file = os.path.join(CACHE_DATA_DIR, sorted(os.listdir(CACHE_DATA_DIR))[-1])
        with open(latest_file, 'r') as f:
            data = json.load(f)

        coll_id = '151215d5-10a7-494d-96cd-5bf7b2bff3b6'  # this will be used in later parse on property key map
        property_key_map = data['recordMap']['collection'][coll_id]['value']['schema']

        raw_items = data['recordMap']['block'].items()
        items: List[NotionHeroModel] = []
        for user_id, user_data in raw_items:

            # 这些应该是空行！
            # self.assertIn('properties', user_data['value'])
            if 'properties' not in user_data['value']: continue

            item = {}
            for key, vals in user_data['value']['properties'].items():
                if key in property_key_map:
                    item[property_key_map[key]['name']] = vals  # 编码列 --> 可读列

            try:
                notion_hero_model = NotionHeroModel(
                    avatar='',
                    id=user_id,
                    name=parse_p1(r'([\u4e00-\u9fa5]+)', item[NOTION_COL_MAP["name"]]),
                    avatar_notion=get_notion_avatar_url(
                        user_id,
                        parse_p1(r"(http.*?)'", item[NOTION_COL_MAP["avatar"]])
                    ),
                    title=parse_p1(r'([\u4e00-\u9fa5]+)', item.get(NOTION_COL_MAP["title"])),
                    cities=parse_p1(r'([\u4e00-\u9fa5]+)', item.get(NOTION_COL_MAP["cities"]))
                )
                items.append(notion_hero_model)
            except Exception as e:
                # pprint(item)
                pass
        print({"stat": {"raw_times": len(raw_items), "parsed": len(items)}})
        return items
