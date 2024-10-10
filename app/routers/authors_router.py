import logging

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from app.crud.authors_crud import AuthorCRUD
from app.dependencies import get_author_collection
from app.schemas.authors_schema import AuthorResponse, AuthorCreate

router = APIRouter()
logging.basicConfig(level=logging.INFO)


def get_author_crud(collection: AsyncIOMotorCollection = Depends(get_author_collection)) -> AuthorCRUD:
    return AuthorCRUD(collection)


@router.post("/authors/", response_model=AuthorResponse, status_code=201, tags=["Authors"])
async def create_author(author_data: AuthorCreate, crud: AuthorCRUD = Depends(get_author_crud)):
    return await crud.create_author(author_data)


@router.get("/authors/{author_id}", response_model=AuthorResponse, tags=["Authors"])
async def get_author(author_id: str, crud: AuthorCRUD = Depends(get_author_crud)):
    author = await crud.get_author(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
