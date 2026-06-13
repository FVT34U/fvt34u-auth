from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from core import settings
import logging


logger = logging.getLogger(__name__)


class AsyncSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._async_session_factory: async_sessionmaker[AsyncSession] | None = None
    
    async def start(self):
        self._engine = create_async_engine(
            settings.DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            echo=False,
        )

        self._async_session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        logger.info("Database connected")

    async def stop(self):
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._async_session_factory = None
            logger.info("Database connection closed")
    
    def get_session(self) -> AsyncSession:
        if not self._async_session_factory:
            raise RuntimeError(
                "AsyncSessionManager not started "
                "Call start() in lifespan method."
            )
        return self._async_session_factory()
    
    @property
    def is_running(self) -> bool:
        return self._engine is not None


async_session_manager = AsyncSessionManager()