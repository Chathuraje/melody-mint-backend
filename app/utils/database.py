import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from app.utils.config import DB_USERNAME, DB_PASSWORD, DB_URL, DB_NAME
from app.utils import logging

logger = logging.getLogger()

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}/?retryWrites=true&w=majority&appName=melody-mint"

# Global variable to store the database connection
db_connection = None


async def connect():
    global db_connection
    try:
        client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
        await client.admin.command("ping")
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        db_connection = client[DB_NAME]  # type: ignore
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")


async def disconnect():
    global db_connection
    if db_connection is not None:  # type: ignore
        db_connection.client.close()  # type: ignore
        logger.info("Disconnected from MongoDB!")


async def get_collection(collection_name):
    global db_connection
    if db_connection is None:
        await connect()  # Connect if not already connected
    return db_connection[collection_name]  # type: ignore
