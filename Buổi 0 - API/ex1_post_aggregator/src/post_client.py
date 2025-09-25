import asyncio
import time
import aiohttp
from typing import List, Optional
from models import Post
from config import POSTS_API, CACHE_TTL_SECONDS, RETRY_LIMIT, RETRY_BASE_DELAY
from logging_utils import get_logger

logger = get_logger("PostClient")

class PostClient:
    _cache: List[Post] = []
    _cache_time: Optional[float] = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_posts(cls) -> List[Post]:
        now = time.time()
        if cls._cache and cls._cache_time and now - cls._cache_time < CACHE_TTL_SECONDS:
            logger.info("Using cached posts")
            return cls._cache

        async with cls._lock:
            now = time.time()
            if cls._cache and cls._cache_time and now - cls._cache_time < CACHE_TTL_SECONDS:
                logger.info("Using cached posts (after lock)")
                return cls._cache

            for attempt in range(1, RETRY_LIMIT + 1):
                try:
                    logger.info(f"Fetching posts attempt {attempt}")
                    async with aiohttp.ClientSession() as session:
                        async with session.get(POSTS_API, timeout=10) as resp:
                            resp.raise_for_status()
                            data = await resp.json()
                            posts = [Post.from_dict(p) for p in data]
                            cls._cache = posts
                            cls._cache_time = time.time()
                            logger.info(f"Fetched {len(posts)} posts")
                            return posts
                except Exception as e:
                    delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    logger.warning(f"Attempt {attempt} failed: {e}; backing off {delay:.1f}s")
                    await asyncio.sleep(delay)
            logger.error("All retry attempts exhausted")
            raise RuntimeError("Failed to fetch posts")
