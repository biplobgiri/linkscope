from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link,Click
from app.schemas import StatsResponse
from collections import Counter

router= APIRouter()

@router.get("/stats/{slug}", response_model=StatsResponse)
async def get_stats(slug:str, db:Session=Depends(get_db)):
    link = db.query(Link).filter(Link.slug==slug).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    clicks=db.query(Click).filter(Click.link_id==link.id).all()

    return StatsResponse(
        slug=link.slug,
        original_url=link.original_url,
        total_clicks=len(clicks),
        is_active=link.is_active,
        created_at=link.created_at,
        expires_at=link.expires_at,
        max_clicks=link.max_clicks,
        clicks=clicks
    )

@router.get("/stats/{slug}/summary")
async def get_stats_summary( slug:str,db:Session=Depends(get_db)):

    link=db.query(Link).filter(Link.slug==slug).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    clicks=db.query(Click).filter(Click.link_id==link.id).all()

    countries=Counter(c.country for c in clicks if c.country)
    referrers=Counter(c.referrer for c in clicks if c.referrer)
    browsers=Counter(c.user_agent for c in clicks if c.user_agent)

    return {
        "slug": link.slug,
        "total_clicks":len(clicks),
        "top_countries":countries.most_common(5),
        "top_referrers":referrers.most_common(5),
        "top_browsers":browsers.most_common(5),
        "clicks_remaining":(link.max_clicks-len(clicks)) if link.max_clicks else None
    }