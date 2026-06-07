from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from core import settings

# TODO: rewrite with class
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=False,
)


AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)