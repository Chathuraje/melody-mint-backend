from pydantic import BaseModel, Field
from typing import Optional

class LogContent(BaseModel):
    logs: Optional[list[str]] = Field(None, description="List of log lines")