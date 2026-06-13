from redis.asyncio import Redis, ConnectionPool
from core import settings
import logging


logger = logging.getLogger(__name__)


class RedisPoolManager:
    def __init__(self):
        self._redis_pool: ConnectionPool | None = None

    async def start(self):
        self._redis_pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=20,
            decode_responses=True,
        )

        logger.info("Redis pool started")
    
    async def stop(self):
        if self._redis_pool:
            await self._redis_pool.aclose()
            self._redis_pool = None

            logger.info("Redis pool closed")

    def get_redis_pool(self) -> ConnectionPool:
        if self._redis_pool is None:
            raise RuntimeError(
                "RedisPoolManager not started "
                "Call start() in lifespan method."
            )
        return self._redis_pool

    @property
    def is_running(self) -> bool:
        return self._redis_pool is not None


redis_pool_manager = RedisPoolManager()

