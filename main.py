from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import auth_router
from core.kafka import kafka_producer
from core.database import engine
import logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("WAKE UP, SUNSHINE!")

    await kafka_producer.start()

    yield

    await kafka_producer.stop()

    await engine.dispose()

    logger.info("GOOD BYE, SWEET PRINCE!")

app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}