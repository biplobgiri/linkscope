from sqlalchemy.orm import Session
from app.models import Click, Link
from app.metrics import total_clicks
import httpx

async def log_click(
        db:Session,
        link:Link,
        ip:str|None,
        user_agent:str|None,
        referrer:str|None
):
    country = await get_country_from_ip(ip)
    
    click=Clicks(
        link_id=link.id,
        ip=ip,
        user_agent=user_agent,
        referrer=referrer,
        country=country
    )

    db.add(click)

    link.clicks
    if link.max_clicks and len(link.clicks)>=link.max_clicks:
        link.is_active=False

    db.commit()

    total_clicks.labels(slug=link.slug).inc()


async def get_country_from_ip(ip:str | None)->str | None:
    if not ip or ip in ("127.0.0.1","localhost","testclient"):
        return None
    try:
        async with httpx.AsyncClient() as client:
            response=await client.get(f"http://ip-api.com/json/{ip}",timeout=3.0)
            data=response.json()
            if data.get("status")=="success":
                return data.get("country")
            
    except Exception:
        return None
