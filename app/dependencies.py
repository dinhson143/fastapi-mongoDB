from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorCollection


async def get_book_collection(request: Request) -> AsyncIOMotorCollection:
    container = request.app.state.container
    book_collection = container.book_collection()
    return book_collection


async def get_author_collection(request: Request) -> AsyncIOMotorCollection:
    container = request.app.state.container
    author_collection = container.author_collection()
    return author_collection


async def create_book_indexes(book_collection: AsyncIOMotorCollection):
    await book_collection.create_index([("title", 1)], unique=True)
    await book_collection.create_index([("price", 1)], unique=True)
    print("Book's indexes created successfully")


