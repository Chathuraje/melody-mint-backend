from fastapi import APIRouter, status
from app.utils import logging
from app.api.v1.libraries.root import root

root_router = APIRouter(tags=["Root"])
logger = logging.getLogger()


@root_router.get(
    "/", description="This is the root endpoint.", status_code=status.HTTP_200_OK
)
async def read_root():
    logger.info("Root endpoint accessed.")
    return await root.read_root()


@root_router.get(
    "/health-check",
    description="This is the health check endpoint.",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    logger.info("Health check endpoint accessed.")
    return await root.health_check()


@root_router.get(
    "/read-log",
    description="This is to read the log file.",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
async def read_log(limit: int = None):  # type: ignore
    logger.info("Read log endpoint accessed.")

    return await root.read_log(limit)
