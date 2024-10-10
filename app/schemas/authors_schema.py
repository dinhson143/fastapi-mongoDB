from bson import ObjectId
from pydantic import BaseModel, root_validator, validator
from typing import Optional


class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorReferenceResponse(BaseModel):
    id: str
    name: str


class AuthorResponse(BaseModel):
    id: str
    name: str
    bio: Optional[str]

    @root_validator(pre=True)
    def convert_objectid_to_str(cls, values):
        if isinstance(values.get('id'), ObjectId):
            values['id'] = str(values['id'])
        return values

    class Config:
        orm_mode = True

