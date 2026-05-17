from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import secrets

class Link(Base):
    __tablename__="links"

    id=Column(Integer, primary_key=True, index= True)
    slug=Column(String,unique=True, index=True, nullable=False)
    original_url=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    expires_at=Column(DateTime(timezone=True),nullable=True)
    max_clicks=Column(Integer, nullable=True)
    is_active=Column(Boolean, default=True)

    clicks=relationship("Click", back_populates="link")

    def generate_slug():
        return secrets.token_urlsafe(6)
    
class Click(Base):
    __tablename__="clicks"

    id=Column(Integer,primary_key=True, index=True)
    link_id=Column(Integer,ForeignKey("links.id"),nullable=False)
    ip=Column(String,nullable=True)
    user_agent=Column(String,nullable=True)
    referrer=Column(String, nullable=True)
    country=Column(String, nullable=True)
    clicked_at=Column(DateTime(timezone=True),server_default=func.now())

    link=relationship("Link", back_populates="clicks")

    
