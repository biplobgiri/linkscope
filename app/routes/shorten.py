from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link
from app.schemas import ShortenRequest, ShortenResponse
from app.services.cache import set_cached_url
from app.metrics import links_created, active_links
import os

router= APIRouter()

@router.post("/shorten",response_model=ShortenResponse)
async def shorten_url(request: ShortenRequest, db:Session=Depends(get_db)):
    slug=request.custom_slug or Link.generate_slug()

    existing=db.query(Link).filter(Link.slug==slug).first()
    if existing:
        raise HTTPException(status_code=400,detail="Slug already taken, try different one ")
    
    link=Link(
        slug=slug,
        original_url=str(request.original_url),
        expires_at=request.expires_at,
        max_clicks=request.max_clicks
    )

    db.add(link)
    db.commit()
    db.refresh(link)

    await set_cached_url(
        slug=slug,
        original_url=str(request.original_url),
        ttl=3600
    )

    links_created.inc()
    active_links.inc()

    base_url=os.getenv("BASE_URL","http://localhost:8000")

    return ShortenResponse(
        slug=slug,
        short_url=f"{base_url}/r/{slug}",
        original_url=str(request.original_url),
        expires_at=link.expires_at,
        max_clicks=link.max_clicks
    )