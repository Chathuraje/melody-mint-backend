from app.utils import logging
from app.utils.database import connect


async def startup_event():
    logging.setupLogger()
    logger = logging.getLogger()

    # Connect to MongoDB
    await connect()

    logger.info(f"Melody Mint FastAPI running....")
