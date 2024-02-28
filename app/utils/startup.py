from app.utils import logging


async def startup_event():
    logging.setup_logger()
    logger = logging.get_logger()
    
    STAGE = "DEVELOPMENT"
    logger.info(f"Running...: MODE - {STAGE}")