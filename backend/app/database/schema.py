from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DetectionResponse(BaseModel):
    id: int
    timestamp: datetime
    people_count: int
    result_image_url: str
    original_filename: str
    
    class Config:
        orm_mode = True

class DetectionHistory(BaseModel):
    id: int
    timestamp: datetime
    people_count: int
    result_image_url: str
    original_filename: str
    
    class Config:
        orm_mode = True

class PaginatedResponse(BaseModel):
    items: List[DetectionHistory]
    total: int
    page: int
    size: int