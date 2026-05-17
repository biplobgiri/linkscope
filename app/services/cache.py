import redis.asyncio as aioredis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_cached_url(slug: str) -> str | None:
    return await redis_client.get(f"slug:{slug}")

async def set_cached_url(slug: str, original_url: str, ttl: int = 3600):
    await redis_client.set(f"slug:{slug}", original_url, ex=ttl)

async def delete_cached_url(slug: str):
    await redis_client.delete(f"slug:{slug}")

async def is_redis_alive() -> bool:
    try:
        await redis_client.ping()
        return True
    except Exception:
        return False