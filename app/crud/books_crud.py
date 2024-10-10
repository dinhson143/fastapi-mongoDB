from typing import Optional, List

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.books_model import BookModel
from app.models.py_object_id import PyObjectId
from app.schemas.books_schema import CreateBookSchema, UpdateBookSchema, BookResponseSchema, ListBooksSchema
from app.utils.logger import logger


class BookCRUD:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_book(self, book_data: CreateBookSchema) -> str:
        try:
            new_book = BookModel(**book_data.dict())
            result = await self.collection.insert_one(new_book.dict(by_alias=True))
            new_book.id = result.inserted_id
            logger.info(f"Book created with ID: {new_book.id}")
            return str(new_book.id)
        except Exception as e:
            logger.error(f"Error while creating book: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to create book due to an internal error: {e}")

    async def get_book(self, book_id: str) -> Optional[BookResponseSchema]:
        try:
            book = await self.collection.find_one({"_id": PyObjectId(book_id)})
            if book:
                logger.info(f"Book found with ID: {book_id}")
                return BookResponseSchema.from_mongo(book)
            logger.warning(f"Book not found with ID: {book_id}")
            return None
        except Exception as e:
            logger.error(f"Error while getting book with ID {book_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve book due to an internal error: {e}")

    async def list_books(self, skip: int = 0, limit: int = 10) -> Optional[List[BookResponseSchema]]:
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            books_list = await cursor.to_list(length=limit)
            if not books_list:
                logger.warning(f"Books not found")
                raise HTTPException(status_code=404, detail="No books found")
            return [BookResponseSchema.from_mongo(book) for book in books_list]
        except Exception as e:
            logger.error(f"ERROR: while listing books: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to list books due to an internal error: {e}")

    async def update_book(self, book_id: str, update_data: UpdateBookSchema) -> Optional[BookResponseSchema]:
        try:
            update_dict = update_data.dict()
            result = await self.collection.update_one({"_id": PyObjectId(book_id)}, {"$set": update_dict})
            if result.modified_count > 0:
                updated_book = await self.get_book(book_id)
                logger.info(f"Book with ID {book_id} updated successfully")
                return updated_book
            logger.warning(f"No updates applied for book with ID: {book_id}")
            raise HTTPException(status_code=304, detail=f"No updates were applied to book with ID {book_id}.")
        except Exception as e:
            logger.error(f"Error while updating book with ID {book_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to update book due to an internal error: {e}")

    async def delete_book(self, book_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": PyObjectId(book_id)})
            if result.deleted_count > 0:
                logger.info(f"Book with ID {book_id} deleted successfully")
                return True
            logger.warning(f"Book with ID {book_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found for deletion.")
        except Exception as e:
            logger.error(f"Error while deleting book with ID {book_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to delete book due to an internal error: {e}")

    async def get_book_by_title(self, title: str) -> Optional[BookResponseSchema]:
        try:
            book = await self.collection.find_one({"title": title})
            if book:
                logger.info(f"Book found with title: {title}")
                return BookResponseSchema.from_mongo(book)
            logger.warning(f"Book not found with title: {title}")
            return None
        except Exception as e:
            logger.error(f"Error while getting book with title {title}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve book due to an internal error: {e}")

    async def get_books_by_book_type_genre_rating(self, book_type: str, genre: str, min_rating: float, max_rating: float) -> List[BookResponseSchema]:
        try:
            query = {
                "book_type": book_type,
                "genre": genre,
                "average_rating": {"$gte": min_rating, "$lte": max_rating}
            }
            books = await self.collection.find(query).to_list(length=None)
            if books:
                logger.info(f"Books found for book_type: {book_type}, genre: {genre}, rating: {min_rating} - {max_rating}")
                return [BookResponseSchema.from_mongo(book) for book in books]
            logger.warning(f"No books found for book_type: {book_type}, genre: {genre}, rating: {min_rating} - {max_rating}")
            return []
        except Exception as e:
            logger.error(f"Error while getting books with book_type {book_type}, genre {genre}, rating {min_rating} - {max_rating}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve books due to an internal error: {e}")

    async def get_books_sorted_by_price(self) -> List[BookResponseSchema]:
        try:
            books = await self.collection.find().sort("price", 1).to_list(length=None)
            if books:
                logger.info("Books retrieved and sorted by price.")
                return [BookResponseSchema.from_mongo(book) for book in books]

            logger.warning("No books found.")
            return []
        except Exception as e:
            logger.error(f"Error while getting books sorted by price: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve books due to an internal error: {e}")

    async def get_books_by_price_range(self, min_price: float, max_price: float) -> List[BookResponseSchema]:
        try:
            books = await self.collection.find({"price": {"$gte": min_price, "$lte": max_price}}).to_list(length=100)
            logger.info(f"Retrieved {len(books)} books with price between {min_price} and {max_price}.")
            return [BookResponseSchema.from_mongo(book) for book in books]
        except Exception as e:
            logger.error(f"Error while retrieving books by price range: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve books due to an internal error: {e}")




