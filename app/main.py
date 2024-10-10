import os

from fastapi import FastAPI
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorClient

from app.container import Container
from app.routers import books_router, authors_router

app = FastAPI(
    title="BookStore API",
    description="API for managing books and authors",
    version="1.0.0",
)
# Database
container = Container()
container.config.mongodb.url.from_value(os.getenv("MONGODB_URL"))
app.state.container = container

app.include_router(books_router.router)
app.include_router(authors_router.router)


@app.on_event("startup")
async def startup_event():
    db_client: AsyncIOMotorClient = container.db_client()
    try:
        await db_client.admin.command('ping')
        print("MongoDB connection successful.")
        # book_collection = container.book_collection()
        # await create_book_indexes(book_collection)
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e


@app.on_event("shutdown")
async def shutdown_event():
    await container.db_client().close()


@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI project!"}


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
