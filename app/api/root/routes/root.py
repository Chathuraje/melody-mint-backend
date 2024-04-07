from fastapi import APIRouter
from app.utils import logging
from app.api.root.libraries import root

logger = logging.getLogger()
router = APIRouter()


@router.get("/", description="This is the root endpoint.")
async def read_root():
    logger.info("Root endpoint accessed.")

    return await root.read_root()


@router.get(
    "/read-log", description="This is to read the log file.", response_model=list[str]
)
async def read_log(limit: int = None):  # type: ignore
    logger.info("Read log endpoint accessed.")

    return await root.read_log(limit)
