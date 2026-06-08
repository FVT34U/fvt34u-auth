from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import auth_router
from core.kafka import kafka_producer_manager
from core.database import async_session_manager
from core.redis import redis_pool_manager
import logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("WAKE UP, SUNSHINE!")

    await kafka_producer_manager.start()
    await async_session_manager.start()
    await redis_pool_manager.start()

    yield

    await kafka_producer_manager.stop()
    await async_session_manager.stop()
    await redis_pool_manager.stop()

    logger.info("GOOD BYE, SWEET PRINCE!")

app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}