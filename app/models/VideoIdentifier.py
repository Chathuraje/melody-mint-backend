from pydantic import BaseModel, Field
from typing import Optional

class Video(BaseModel):
    title: Optional[str] = Field(..., description="Title of the video")
    artist: Optional[str] = Field(..., description="Artist of the video")
    duration: Optional[str] = Field(..., description="Duration of the video")
    genre: Optional[str] = Field(..., description="Genre of the video")

class VideoReturn(Video):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
class VideoNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")