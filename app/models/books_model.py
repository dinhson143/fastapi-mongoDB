from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.authors_model import AuthorReference
from app.models.py_object_id import PyObjectId
from app.utils.book_enum import BookTypeEnum
from app.utils.book_enum import Genre


class BookModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    title: str
    author_ids: List[AuthorReference]  # Extended Reference Pattern
    book_type: Optional[BookTypeEnum] = BookTypeEnum.PAPERBACK  # Inheritance Pattern
    genre: Optional[List[Genre]] = [Genre.FANTASY]
    price: Optional[float] = 0
    stock: Optional[int] = 0
    average_rating: Optional[float] = 5
    version: Optional[int] = 1  # Schema versioning

    # Specific fields for Ebook
    file_format: Optional[str] = None
    file_size: Optional[float] = None

    # Specific fields for Audiobook
    duration: Optional[int] = None
    narrator: Optional[str] = None

    # Specific fields for Paperback
    weight: Optional[float] = None
    dimensions: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
