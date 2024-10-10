import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.crud.books_crud import BookCRUD
from app.dependencies import get_book_collection
from app.schemas.books_schema import CreateBookSchema, UpdateBookSchema, BookResponseSchema, ListBooksSchema

router = APIRouter()
logging.basicConfig(level=logging.INFO)


def get_book_crud(collection: AsyncIOMotorCollection = Depends(get_book_collection)) -> BookCRUD:
    return BookCRUD(collection)


@router.post("/books/", response_model=str, status_code=status.HTTP_201_CREATED, tags=["Books"])
async def create_book(book_data: CreateBookSchema, crud: BookCRUD = Depends(get_book_crud)):
    return await crud.create_book(book_data)


@router.get("/books/{book_id}", response_model=BookResponseSchema, tags=["Books"])
async def get_book(book_id: str, crud: BookCRUD = Depends(get_book_crud)):
    book = await crud.get_book(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("/books/title/{title}", response_model=BookResponseSchema, tags=["Books"])
async def get_book_by_title(title: str, crud: BookCRUD = Depends(get_book_crud)):
    book = await crud.get_book_by_title(title)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("/books/sorted-by-price/", response_model=List[BookResponseSchema], tags=["Books"])
async def get_books_sorted_by_price(crud: BookCRUD = Depends(get_book_crud)):
    books = await crud.get_books_sorted_by_price()
    if not books:
        raise HTTPException(status_code=404, detail="No books found.")
    return books


@router.get("/books/", response_model=List[BookResponseSchema], tags=["Books"])
async def list_books(skip: int = 0, limit: int = 10, crud: BookCRUD = Depends(get_book_crud)):
    return await crud.list_books(skip=skip, limit=limit)


@router.put("/books/{book_id}", response_model=BookResponseSchema, tags=["Books"])
async def update_book(book_id: str, book_data: UpdateBookSchema, crud: BookCRUD = Depends(get_book_crud)):
    updated_book = await crud.update_book(book_id, book_data)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found or not updated")
    return updated_book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
async def delete_book(book_id: str, crud: BookCRUD = Depends(get_book_crud)):
    success = await crud.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return


@router.get("/books/price-range/", response_model=List[BookResponseSchema], tags=["Books"])
async def get_books_by_price_range(min_price: float, max_price: float, crud: BookCRUD = Depends(get_book_crud)):
    books = await crud.get_books_by_price_range(min_price, max_price)
    if not books:
        raise HTTPException(status_code=404, detail="No books found in the specified price range.")
    return books
