import os
import uuid
from typing import Union

import requests
from PIL import Image
from fastapi import UploadFile, Path, HTTPException, Depends
from fastapi.routing import APIRouter
from starlette.responses import FileResponse

from api.hero.ds import HeroModel
from log import getLogger
from packages.general.db import coll_hero
from path import UPLOADED_DATA_DIR, UPLOADED_THUMB_DATA_DIR

files_router = APIRouter(prefix="/files", tags=["files"])

logger = getLogger("API_Files")


def get_uploaded_file_list():
    return os.listdir(UPLOADED_DATA_DIR)


def get_uploaded_first_file() -> Union[str, None]:
    for file_id in os.listdir(UPLOADED_DATA_DIR):
        return file_id
    return None


def get_uploaded_file_path_from_id(file_id: str, raw=False):
    return os.path.join(UPLOADED_DATA_DIR if raw else UPLOADED_THUMB_DATA_DIR, file_id)


def write_image(filename, filedata) -> str:
    # todo: 不确定能不能用中文名， htmltoimage 相关
    # file_id = f'{uuid.uuid1()}_{filename}'
    # 要有后缀，否则 Image 不知道怎么读
    file_id = uuid.uuid1().__str__() + ".png"

    # dump raw
    logger.info(f'writing raw image of id={file_id}')
    raw_img_path = os.path.join(UPLOADED_DATA_DIR, file_id)
    with open(raw_img_path, "wb") as f:
        f.write(filedata)

    # dump thumb
    logger.info(f'writing thumb image of id={file_id}')
    img = Image.open(raw_img_path)
    w, h = img.size
    MAX_W = 360
    # todo: avoid write if w <= MAX_W, but how do we change the api ?
    h = int(h / w * MAX_W)
    w = MAX_W
    img.resize((w, h)).save(
        os.path.join(UPLOADED_THUMB_DATA_DIR, file_id)
    )
    return os.environ['BACKEND_ENDPOINT'] + "/files/" + file_id


@files_router.post("/upload", description='返回上传后的id', )
async def upload(file: UploadFile):
    """
    todo: support duplication detect using Redis/Cache
    :param file:
    :return:
    """
    return write_image(file.filename, file.file.read())


@files_router.get("/list")
async def get_list():
    files_list = get_uploaded_file_list()
    return files_list


@files_router.delete('/clear')
async def clear_uploaded_files():
    dirs = [UPLOADED_DATA_DIR, UPLOADED_THUMB_DATA_DIR]
    ret = dict((i, 0) for i in dirs)
    for dir in dirs:
        os.chdir(dir)
        for filename in os.listdir(dir):
            os.remove(filename)
            ret[dir] += 1
    return ret


@files_router.get("/{file_id}")
async def get_file(file_id: str = Path(), raw=False):
    logger.info(f'reading file id={file_id}')
    file_path = get_uploaded_file_path_from_id(file_id, raw)
    logger.info({"file_id": file_id, "file_path": file_path})
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail=f"not found file of id={file_id}")


@files_router.get('/external/check')
async def check_external():
    items = list(coll_hero.find({"avatar": {"$regex": "notion"}}))
    return items


@files_router.post('/external/handle')
async def handle_external(res=Depends(check_external)):
    data = res["data"]["data"]
    data_new = []
    for item in data:
        # todo: 实现一个UploadFile
        res = requests.get(item['avatar'])
        return write_image(f'{item["name"]}.png', res.content)
