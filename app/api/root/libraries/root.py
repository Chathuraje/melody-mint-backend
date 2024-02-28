from fastapi import HTTPException
from app.utils.response import StandardResponse, LogContent, ReadLogResponse
from app.utils.logging import setup_logger, get_logger
import aiofiles
import traceback
from collections import deque 

setup_logger()
logger = get_logger()


# SECTION: FastAPI Logs
async def read_log(limit) -> ReadLogResponse:
    try:
        async with aiofiles.open("melodymint.log", "r") as log_file:
            if limit is None or limit < 0:
                 log_content = [line.strip() async for line in log_file]
            else:
                log_content = deque(await log_file.readlines(), maxlen=limit)
                log_content = list(log_content)
                
        return ReadLogResponse(code=200, data=LogContent(logs=log_content))

    except FileNotFoundError as e:
        logger.error(f"Log file not found: {e}")
        raise HTTPException(status_code=404, detail=f"Log file not found: {e}") from e
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Error while reading log file: {e}\nTraceback: {tb}")
        raise HTTPException(status_code=500, detail=f"Error while reading log file: {e}\nTraceback: {tb}") from e