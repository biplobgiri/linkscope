from pydantic import BaseModel, HttpUrl, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class ShortenRequest(BaseModel):
    original_url: HttpUrl
    custom_slug: Optional[str] = None
    max_clicks: Optional[int] = None
    expires_at: Optional[datetime] = None



class ShortenResponse(BaseModel):
    slug: str
    short_url: str
    original_url: str
    expires_at: Optional[datetime] = None
    max_clicks: Optional[int] = None

    @field_validator("original_url")
    @classmethod
    def validate_url(cls,v):
        if not v.startswith("http://") and not v.startswith("https://"):
            v="https://"+v
        return v
     
class ClickResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ip: Optional[str]
    referrer: Optional[str]
    country: Optional[str]
    clicked_at: datetime

class StatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    original_url: str
    total_clicks: int
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    max_clicks: Optional[int]
    clicks: list[ClickResponse] = []