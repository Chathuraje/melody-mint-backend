from pydantic import BaseModel, Field
from typing import Optional, List

class Music(BaseModel):
    title: Optional[str] = Field(..., description="Title of the music")
    duration: Optional[str] = Field(..., description="Duration of the music")
    uploader_id: Optional[str] = Field(..., description="Uploader ID of the music")
    uploader_name: Optional[str] = Field(..., description="Uploader name of the music")

class MusicReturn(Music):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
class MusicNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")