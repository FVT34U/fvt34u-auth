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

    async def publish(self, topic: str, value: dict) -> None:
        if not self._producer:
            raise RuntimeError("Kafka producer не запущен")
        await self._producer.send_and_wait(topic, value)

    @property
    def is_running(self) -> bool:
        return self._producer is not None


kafka_producer = KafkaProducerManager()