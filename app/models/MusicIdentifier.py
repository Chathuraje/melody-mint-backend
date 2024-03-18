from pydantic import BaseModel, Field
from typing import Optional, List, Any

class Music(BaseModel):
    title: Optional[str] = Field(..., description="Title of the music")

class MusicReturn(Music):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
class MusicNew(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    
    
class Records(BaseModel):
    date: Optional[str] = Field(..., description="Date of the music")
    time: Optional[str] = Field(..., description="Time of the music")
    duration: Optional[str] = Field(..., description="Duration of the music")

class PlatformDetails(BaseModel):
    platform_name: Optional[str] = Field(..., description="Platform name of the music")
    stream_count: Optional[int] = Field(..., description="Stream of the music")
    records: Optional[List[Records]] = Field(..., description="Records of the music")
    
class MusicResponse(BaseModel):
    id: Optional[str] = Field(..., description="Unique ID of the campaigns")
    title: Optional[str] = Field(..., description="Title of the music")
    user_id: Optional[str] = Field(..., description="User ID of the music")
    type: Optional[str] = Field(..., description="Type of the music")
    total_stream: Optional[int] = Field(..., description="Total streams of the music")
    total_platform: Optional[int] = Field(..., description="Total platforms of the music")
    total_time: Optional[int] = Field(..., description="Total time of the music")
    platform_details: Optional[list[PlatformDetails]] = Field(..., description="Platform details of the music")
    