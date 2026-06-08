from services import AuthService

from aiokafka import AIOKafkaProducer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.kafka import kafka_producer_manager
from core.redis import redis_pool_manager
from core.database import async_session_manager


async def get_auth_service() -> AuthService:
    pass


async def get_kafka_producer() -> AIOKafkaProducer:
    yield kafka_producer_manager.get_producer()


async def get_redis() -> Redis:
    async with Redis(connection_pool=redis_pool_manager.get_redis_pool()) as redis:
        yield redis


async def get_async_session() -> AsyncSession:
    async with async_session_manager.get_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise