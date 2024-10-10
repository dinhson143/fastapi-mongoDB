from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, root_validator, Field

from app.schemas.authors_schema import AuthorReferenceResponse
from app.utils.book_enum import BookTypeEnum
from app.utils.book_enum import Genre


class CreateBookSchema(BaseModel):
    title: str
    author_ids: List[AuthorReferenceResponse]
    book_type: BookTypeEnum = BookTypeEnum.PAPERBACK
    genre: List[Genre] = Field(default_factory=lambda: [Genre.FANTASY])
    price: Optional[float] = 0
    stock: Optional[int] = 0
    average_rating: Optional[float] = 5
    version: Optional[int] = 1

    file_format: Optional[str] = None
    file_size: Optional[float] = None

    duration: Optional[int] = None
    narrator: Optional[str] = None

    weight: Optional[float] = None
    dimensions: Optional[str] = None


class UpdateBookSchema(BaseModel):
    title: Optional[str] = None
    author_ids: Optional[List[AuthorReferenceResponse]] = None
    book_type: Optional[BookTypeEnum] = None
    genre: Optional[List[Genre]] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    file_format: Optional[str] = None
    file_size: Optional[float] = None

    duration: Optional[int] = None
    narrator: Optional[str] = None

    weight: Optional[float] = None
    dimensions: Optional[str] = None


class BookResponseSchema(BaseModel):
    id: str
    title: str
    author_ids: List[AuthorReferenceResponse]
    book_type: BookTypeEnum
    genre: List[Genre]
    price: float
    stock: int
    average_rating: float
    version: int

    file_format: Optional[str] = None
    file_size: Optional[float] = None

    duration: Optional[int] = None
    narrator: Optional[str] = None

    weight: Optional[float] = None
    dimensions: Optional[str] = None

    @classmethod
    def from_mongo(cls, book_data):
        book_data['id'] = str(book_data['_id'])
        book_data['author_ids'] = [
            AuthorReferenceResponse(
                id=str(author['_id']) if '_id' in author else author['id'],
                name=author['name']
            )
            for author in book_data.get('author_ids', [])
        ]
        return cls(**book_data)

    class Config:
        orm_mode = True


class ListBooksSchema(BaseModel):
    books: List[BookResponseSchema]
    total: int
