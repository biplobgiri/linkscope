from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class ShortenRequest(BaseModel):
    original_url:HttpUrl
    custom_slug: Optional[str]=None
    max_clicks:Optional[int]=None
    expires_at:Optional[datetime]=None

class ShortenResponse(BaseModel):
    slug:str
    short_url:str
    original_url:str
    expires_at: Optional[datetime]=None
    max_clicks:Optional[int]=None

class ClickResponse(BaseModel):
    ip:Optional[str]
    referrer:Optional[str]
    country:Optional[str]
    clicked_at:datetime

    class Config:
        from_attributes=True

class StatsResponse(BaseModel):
    slug:str
    original_url:str
    total_clicks:int
    is_active:bool
    created_at: datetime
    expires_at: Optional[datetime]
    max_clicks:Optional[int]
    clicks:list[ClickResponse]=[]

    class Config:
        from_attributes=True

