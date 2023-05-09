import os
from typing import Union

from PIL import Image

from src.libs.log import getLogger
from src.libs.path import UPLOADED_DIR, UPLOADED_THUMB_DATA_DIR

logger = getLogger("file-util")


def get_uploaded_file_list():
    return os.listdir(UPLOADED_DIR)


def get_uploaded_first_file() -> Union[str, None]:
    for file_id in os.listdir(UPLOADED_DIR):
        return file_id
    return None


def get_uploaded_file_path_from_id(file_id: str, raw=False):
    return os.path.join(UPLOADED_DIR if raw else UPLOADED_THUMB_DATA_DIR, file_id)


def get_server_image_path(file_id: str) -> str:
    return "/files/" + file_id


def write_image(file_id, filedata) -> str:
    # dump raw
    logger.info(f'writing raw image of id={file_id}')
    raw_img_path = os.path.join(UPLOADED_DIR, file_id)
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
    return get_server_image_path(file_id)
