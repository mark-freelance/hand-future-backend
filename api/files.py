import os
import uuid
from dataclasses import Field
from typing import Union

from fastapi import UploadFile, Path, HTTPException
from fastapi.routing import APIRouter
from starlette.responses import FileResponse

from api.ds import BaseResSuccessModel, STATUS_OK, ListResModel
from config import URI
from path import UPLOADED_DATA_DIR

files_router = APIRouter(prefix="/files", tags=["files"])


def get_uploaded_file_list():
    return os.listdir(UPLOADED_DATA_DIR)


def get_uploaded_first_file() -> Union[str, None]:
    for file_id in os.listdir(UPLOADED_DATA_DIR):
        return file_id
    return None


def get_uploaded_file_path_from_id(file_id: str):
    return os.path.join(UPLOADED_DATA_DIR, file_id)


@files_router.post("/upload", response_model=BaseResSuccessModel[str])
async def upload(file: UploadFile):
    """
    todo: support duplication detect using Redis/Cache
    :param file:
    :return:
    """
    file_id = f'{uuid.uuid1()}_{file.filename}'
    file_path = os.path.join(UPLOADED_DATA_DIR, file_id)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {
        "status": STATUS_OK,
        "data": f'{URI}/files/{file_id}'
    }


@files_router.get("/list", response_model=ListResModel[str])
async def get_list():
    files_list = get_uploaded_file_list()
    return {
        "status": STATUS_OK,
        "data": {
            "size": files_list.__len__(),
            "data": files_list
        }
    }


@files_router.get("/{file_id}")
async def get_file(file_id: str = Path(
    example=get_uploaded_first_file()
)):
    file_path = get_uploaded_file_path_from_id(file_id)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail=f"not found file of id={file_id}")
