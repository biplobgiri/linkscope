import redis.asyncio as aioredis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client

async def get_cached_url(slug: str) -> str | None:
    try:
        return await get_redis_client().get(f"slug:{slug}")
    except Exception:
        return None

async def set_cached_url(slug: str, original_url: str, ttl: int = 3600):
    try:
        await get_redis_client().set(f"slug:{slug}", original_url, ex=ttl)
    except Exception:
        pass

async def delete_cached_url(slug: str):
    try:
        await get_redis_client().delete(f"slug:{slug}")
    except Exception:
        pass

async def is_redis_alive() -> bool:
    try:
        await get_redis_client().ping()
        return True
    except Exception:
        return False