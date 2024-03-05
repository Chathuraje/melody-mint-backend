from pydantic import BaseModel, Field
from typing import Optional, List

class Music(BaseModel):
    title: Optional[str] = Field(..., description="Title of the music")
    artist: Optional[str] = Field(..., description="Artist of the music")
    duration: Optional[str] = Field(..., description="Duration of the music")
    genre: Optional[str] = Field(..., description="Genre of the music")

class MusicReturn(Music):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
class MusicNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")