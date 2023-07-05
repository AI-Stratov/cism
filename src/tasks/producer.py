import json

from aiokafka import AIOKafkaProducer

from src.config import settings


async def produce_task_lq(task_data: dict):
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        value = json.dumps(task_data).encode()
        await producer.send("low_priority_queue", value=value)
    finally:
        await producer.stop()


async def produce_task_hq(task_data: dict):
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        value = json.dumps(task_data).encode()
        await producer.send("high_priority_queue", value=value)
    finally:
        await producer.stop()
