import os

from fastapi import UploadFile, Path, HTTPException
from fastapi.routing import APIRouter
from starlette.responses import FileResponse

from src.libs.file import get_uploaded_file_list, get_uploaded_file_path_from_id, write_image
from src.libs.log import getLogger
from src.libs.path import UPLOADED_DIR, UPLOADED_THUMB_DATA_DIR

files_router = APIRouter(prefix="/files", tags=["files"])

logger = getLogger("API_Files")


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
    dirs = [UPLOADED_DIR, UPLOADED_THUMB_DATA_DIR]
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
