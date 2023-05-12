from __future__ import annotations

from typing import Optional, List, Union

import requests
from pydantic import BaseModel, Field
from starlette.background import BackgroundTasks

from src.ds.user import HeroModel
from src.libs.file import write_image, get_server_image_path


class IdModel(BaseModel):
    id: str


class FileUrlModel(BaseModel):
    url: str


class NotionInnerFileResourceModel(FileUrlModel):
    expiry_time: str


class NotionOuterFileModel(BaseModel):
    type = 'external'
    name: str
    external: FileUrlModel


class NotionInnerFileModel(BaseModel):
    type = 'file'
    name: str
    file: NotionInnerFileResourceModel


NotionFileModel = Union[NotionInnerFileModel, NotionOuterFileModel]


class NotionTextModel(BaseModel):
    content: str
    link: Optional[str]


class NotionRichTextModel(BaseModel):
    type = "text"
    text: NotionTextModel
    plain_text: str
    href: Optional[str]


class BaseNotionPropertyModel(BaseModel):
    id: str
    type: str


class NotionTitlePropertyModel(BaseNotionPropertyModel):
    type = "title"
    title: List[NotionRichTextModel]


class NotionRichTextPropertyModel(BaseNotionPropertyModel):
    type = 'rich_text'
    rich_text: List[NotionRichTextModel]


class NotionFilesPropertyModel(BaseNotionPropertyModel):
    files: List[NotionFileModel]


class NotionRelationPropertyModel(BaseNotionPropertyModel):
    type = 'relation'
    relation: List[IdModel]


PropertyPhotosModel = NotionFilesPropertyModel
PropertyNameModel = NotionTitlePropertyModel
PropertyTitleModel = NotionRichTextPropertyModel
PropertyPartnersModel = NotionRelationPropertyModel


class NotionPagePropertiesModel(BaseModel):
    照片: PropertyPhotosModel
    嘉宾姓名: PropertyNameModel
    title: PropertyTitleModel
    介绍: PropertyTitleModel
    携手嘉宾: PropertyPartnersModel


class NotionModel(BaseModel):
    id: str
    url: str = Field(..., description='notion个人页面网址')
    properties: NotionPagePropertiesModel

    @property
    def name(self) -> str:
        names = [i.plain_text for i in self.properties.嘉宾姓名.title]
        return ', '.join(names)

    @property
    def first_photo(self) -> Optional[str]:
        def get_file_uri(file: NotionFileModel) -> str:
            if file.type == "file":
                return file.file.url
            return file.external.url

        avatars = list(map(get_file_uri, self.properties.照片.files))
        return avatars[0] if avatars else None

    @property
    def title(self) -> str:
        # titles = [i.plain_text for i in self.properties.title.rich_text]
        # 应花姐要求（携手的未来深圳小分队，2023-05-09），先使用「介绍」列
        titles = [i.plain_text for i in self.properties.介绍.rich_text]
        return ", ".join(titles)

    def to_hero_model(self, bt: BackgroundTasks = None) -> HeroModel:
        avatar = self.first_photo
        if avatar:
            image_id = f"{self.id}.png"
            # local persistence in case of CORS Error, and speed up image loading
            if bt:
                bt.add_task(write_image, image_id, requests.get(avatar).content)
            else:
                # write_image(image_id, requests.get(avatar).content)
                pass
            avatar = get_server_image_path(image_id)

        return HeroModel(
            email=self.id,
            is_hero=True,
            name=self.name,
            avatar=avatar,
            title=self.title,
            cities='',  # todo: cities
            partners=[i.id for i in self.properties.携手嘉宾.relation],
        )
