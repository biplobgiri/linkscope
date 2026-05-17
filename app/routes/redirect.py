from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link
from app.services.cache import get_cached_url, set_cached_url,delete_cached_url
from app.services.analytics import log_click
from app.metrics import cache_hits,cache_misses,expired_link_hits,active_links,redirect_latency
from datetime import datetime,timezone
import time

router=APIRouter()

@router.get("/r/{slug}")
async def redirect_url(
    slug: str,
    request: Request,
    background_tasks:BackgroundTasks,
    db:Session=Depends(get_db)
):
    start=time.time()


    cached_url=await get_cached_url(slug)
    if cached_url:
        cache_hits.inc()
        redirect_latency.observe(time.time()-start)
        return RedirectResponse(url=cached_url, status_code=301)
    
    cache_misses.inc()

    link=db.query(Link).filter(Link.slug==slug).first()

    if not Link:
        redirect_latency.observe(time.time()-start)
        return RedirectResponse(url="/not-found",status_code=302)
    
    if not link.is_active:
        expired_link_hits.inc()
        redirect_latency.observe(time.time()-start)
        return RedirectResponse(url="/expired", status_code=302)
    
    if link.expires_at and link.expires_at<datetime.now(timezone.utc):
        link.is_active=False
        db.commit()
        await delete_cached_url(slug)
        active_links.dec()
        expired_link_hits.inc()
        redirect_latency.observe(time.time()-start)
        return RedirectResponse(url="/expired",status_code=302)
    
    await set_cached_url(slug,link.original_url)

    ip=request.client.host
    user_agent=request.headers.get("user-agent")
    referrer=request.headers.get("referer")

    background_tasks.add_task(log_click,db,link,ip,user_agent,referrer)

    redirect_latency.observe(time.time()-start)
    return RedirectResponse(url=link.original_url,status_code=301)