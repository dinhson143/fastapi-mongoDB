import logging
from typing import Optional

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.authors_model import AuthorModel
from app.models.py_object_id import PyObjectId
from app.schemas.authors_schema import AuthorCreate, AuthorResponse

logging.basicConfig(level=logging.INFO)


class AuthorCRUD:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_author(self, author_data: AuthorCreate) -> Optional[AuthorResponse]:
        try:
            new_author = AuthorModel(**author_data.dict())
            result = await self.collection.insert_one(new_author.dict(by_alias=True))
            new_author.id = result.inserted_id
            logging.info(f"Author created with ID: {new_author.id}")
            return AuthorResponse(**new_author.dict())
        except Exception as e:
            logging.error(f"Error while creating author: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to create author due to an internal error: {e}")

    async def get_author(self, author_id: str) -> Optional[AuthorResponse]:
        try:
            author_data = await self.collection.find_one({"_id": PyObjectId(author_id)})
            if author_data:
                return AuthorResponse(**author_data)
            else:
                logging.warning(f"Author with ID {author_id} not found.")
                return None
        except Exception as e:
            logging.error(f"Error while retrieving author with ID {author_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve author due to an internal error: {e}")
