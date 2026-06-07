from services import AuthService

from aiokafka import AIOKafkaProducer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.kafka import kafka_producer, KafkaProducerManager
from core.redis import get_redis_pool
from core.database import AsyncSessionFactory


async def get_auth_service() -> AuthService:
    pass


async def get_kafka_producer() -> KafkaProducerManager:
    yield kafka_producer

# TODO
async def get_redis() -> Redis:
    pool = get_redis_pool()
    async with Redis(connection_pool=pool) as redis:
        yield redis

# TODO
async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise