from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from app.config.settings import get_settings
from app.utils import logging
from motor.motor_asyncio import AsyncIOMotorCollection

logger = logging.getLogger()
env = get_settings()


# Global variable to store the database connection
db_connection = None


async def connect() -> None:
    global db_connection
    try:
        client = AsyncIOMotorClient(env.DB_URI, server_api=ServerApi("1"))
        await client.admin.command("ping")
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        db_connection = client[env.DB_NAME]
    except Exception as e:
        raise e


async def disconnect() -> None:
    global db_connection
    try:
        if db_connection is not None:
            db_connection.client.close()
            logger.info("Closed connection to MongoDB!")
    except Exception as e:
        raise e


async def get_collection(collection_name) -> AsyncIOMotorCollection:
    global db_connection
    try:
        if db_connection is None:
            await connect()
        if db_connection is not None:
            return db_connection[collection_name]
        else:
            raise Exception("Could not find collection in the database.")
    except Exception as e:
        raise e
