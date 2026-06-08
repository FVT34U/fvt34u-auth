from aiokafka import AIOKafkaProducer
from core import settings
import json
import logging


logger = logging.getLogger(__name__)


class KafkaProducerManager:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None
    
    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode(),
        )
        await self._producer.start()
        logger.info("Kafka producer started")

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None
            logger.info("Kafka producer stopped")

    def get_producer(self) -> AIOKafkaProducer:
        if not self._producer:
            raise RuntimeError(
                "KafkaProducerManager not started "
                "Call start() in lifespan method."
            )
        return self._producer

    @property
    def is_running(self) -> bool:
        return self._producer is not None


kafka_producer_manager = KafkaProducerManager()