from fastapi import HTTPException
from app.utils import logging
import aiofiles
import traceback
from collections import deque

logger = logging.getLogger()


# ROUTE: Root Path
async def read_root() -> str:
    return "Hello World"


# ROUTE: FastAPI Logs
async def read_log(limit) -> list[str]:
    try:
        async with aiofiles.open("system.log", "r") as log_file:
            if limit is None or limit < 0:
                log_content = [line.strip() async for line in log_file]
            else:
                log_content = deque(await log_file.readlines(), maxlen=limit)
                log_content = list(log_content)

            return log_content

    except FileNotFoundError as e:
        logger.error(f"Log file not found: {e}")
        raise HTTPException(status_code=404, detail=f"Log file not found: {e}") from e
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Error while reading log file: {e}\nTraceback: {tb}")
        raise HTTPException(
            status_code=500,
            detail=f"Error while reading log file: {e}\nTraceback: {tb}",
        ) from e
