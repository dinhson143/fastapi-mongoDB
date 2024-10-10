from bson import ObjectId
from pydantic import GetJsonSchemaHandler


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object ID")
        return v

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: dict, handler: GetJsonSchemaHandler) -> dict:
        schema.update(type="string")
        return schema

    def __str__(self):
        return str(self)
