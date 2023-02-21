# quote avatar in db in case of CORS problem
import os.path
from urllib.parse import quote, unquote

import requests

from packages.general.db import coll_hero
from path import AVATAR_DATA_DIR

"""
用以解决当时文件命名没有 `quote` 导致的 image uri 无法被前端顺利访问（CORS）的问题：
 http://gkleifeng.com:3001/files/e28f823e-b064-11ed-aafd-5783702bc47d_%E5%91%A8%E6%A6%95.png
"""

id2name = {}
index = 0
for item in coll_hero.find({}):
    index += 1
    avatar = item['avatar']
    res = requests.get(avatar + "?raw=true")
    name = item['name']
    with open(os.path.join('/Users/mark/Coding/WebstormProjects/react-force-graph/example/img-nodes/avatar',
                           f"{index:03}.png"
                           ), 'wb'
              ) as f:
        f.write(res.content)
    id2name[f'{index:03}.png'] = name

import json

with open("id2name.json", "w") as f:
    json.dump(id2name, f, ensure_ascii=False, indent=2)
