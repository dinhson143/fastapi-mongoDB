from typing import Optional

from pydantic import BaseModel, Field, constr

from app.models.py_object_id import PyObjectId


class AuthorReference(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str


class AuthorModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    name: constr(
        min_length=1,
        max_length=100,
        strip_whitespace=True,
        pattern=r'^[\w\s.,-]+$'
    )
    bio: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
