from app.utils import logging
from config.database import connect


async def startup_event() -> None:
    logging.setupLogger()

    try:
        logger = logging.getLogger()
        logger.info("Melody Mint FastAPI starting...")

        # Connect to MongoDB
        await connect()

        logger.info(f"Melody Mint FastAPI running....")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
