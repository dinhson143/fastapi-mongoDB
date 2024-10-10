from dependency_injector import containers, providers
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


class Container(containers.DeclarativeContainer):
    # Database client
    config = providers.Configuration()

    db_client = providers.Singleton(
        AsyncIOMotorClient,
        config.mongodb.url
    )

    book_collection = providers.Factory(
        lambda client: client["book_store"]["books"],
        db_client
    )

    author_collection = providers.Factory(
        lambda client: client["book_store"]["authors"],
        db_client
    )


