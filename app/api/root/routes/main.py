from fastapi import APIRouter, HTTPException
from app.utils.logging import setup_logger, get_logger
from app.api.root.libraries import root
from app.utils.response import StandardResponse, ReadLogResponse
from fastapi.responses import StreamingResponse

setup_logger()
logger = get_logger()


routers = APIRouter(
    tags=["Root"]
)

@routers.get("/", response_model=StandardResponse)
async def read_root():
    logger.info("Root endpoint accessed.")
    return await root.read_root()

@routers.get("/read-log", response_model=ReadLogResponse)
async def read_log(limit: int = None):
    logger.info("Read log endpoint accessed.")
    return await root.read_log(limit)
