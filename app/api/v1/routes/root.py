from fastapi import APIRouter
from app.utils import logging
from app.api.v1.libraries.root import root

root_router = APIRouter(tags=["Root"])
logger = logging.getLogger()


@root_router.get("/", description="This is the root endpoint.")
async def read_root():
    logger.info("Root endpoint accessed.")
    return await root.read_root()


@root_router.get(
    "/read-log", description="This is to read the log file.", response_model=list[str]
)
async def read_log(limit: int = None):  # type: ignore
    logger.info("Read log endpoint accessed.")

    return await root.read_log(limit)
