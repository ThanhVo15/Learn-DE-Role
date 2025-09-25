from typing import List, Dict
from models import Post
from logging_utils import get_logger

logger = get_logger("PostAggregator")

class PostAggregator:
    @staticmethod
    def count_per_user(posts: List[Post]) -> Dict[int, int]:
        counter: Dict[int, int] = {}
        for p in posts:
            counter[p.userId] = counter.get(p.userId, 0) + 1
        logger.info(f"Aggregated counts for {len(counter)} users")
        return counter

    @staticmethod
    def top_n(counter: Dict[int, int], n=3):
        result = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)[:n]
        logger.info(f"Top {n}: {result}")
        return result
