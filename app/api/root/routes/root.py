from fastapi import APIRouter, HTTPException
from app.utils.logging import setup_logger, get_logger
from app.api.root.libraries import root
from app.utils.response import StandardResponse, ReadLogResponse
from fastapi.responses import StreamingResponse

setup_logger()
logger = get_logger()


router = APIRouter()

@router.get("/", response_model=StandardResponse)
async def read_root():
    logger.info("Root endpoint accessed.")
    return StandardResponse(code=200, data="Hello, this is your FastAPI application!")

@router.get("/read-log", response_model=ReadLogResponse)
async def read_log(limit: int = None):
    logger.info("Read log endpoint accessed.")
    log_content = await root.read_log(limit)
    
    return ReadLogResponse(code=200, data=log_content)
