from unittest import TestCase

from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    id: str = Field(..., alias="_id")
    name: str


class Model2(BaseModel):
    id: str = Field(..., alias="_id")
    name: str

    class Config:
        allow_population_by_field_name = True  # ref: https://docs.pydantic.dev/latest/usage/model_config/#options


class TestModel(TestCase):
    def test_model_field__id(self):
        model = Model(_id="xx", name='yy')
        assert model.id == "xx"
        assert model.name == 'yy'
        assert "_id" not in model

        model = Model.parse_obj({"_id": "xx", "name": "yy"})
        assert model.id == "xx"
        assert model.name == 'yy'
        assert "_id" not in model

    def test_model_field_id(self):
        self.assertRaises(ValidationError, lambda: Model.parse_obj({"id": "xx", "name": "yy"}))

    def test_model2_field_id(self):
        model = Model2(id='xx', name='yy')
        assert model.id == "xx"
        assert model.name == 'yy'
        assert "_id" not in model
        assert "id" in model.dict() and "_id" not in model.dict()
        assert "_id" in model.dict(by_alias=True) and "id" not in model.dict(by_alias=True)
