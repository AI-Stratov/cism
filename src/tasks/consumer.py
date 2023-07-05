import asyncio
import json
from aiokafka import AIOKafkaConsumer
from src.config import settings
from src.tasks.processing import process_task
from logger_config import logger


async def consume_tasks():
    high_consumer = AIOKafkaConsumer(
        'high_priority_queue',
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    low_consumer = AIOKafkaConsumer(
        'low_priority_queue',
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    await high_consumer.start()
    await low_consumer.start()

    try:
        async def process_high_priority_task(high_msg):
            task_data = json.loads(high_msg.value.decode())
            await process_task(task_data)
            logger.info(f"Task was send to high priority")

        async def process_low_priority_task(low_msg):
            task_data = json.loads(low_msg.value.decode())
            await asyncio.sleep(15)
            await process_task(task_data)
            logger.info(f"Task was send to low priority")

        async def consume():
            async for high_msg in high_consumer:
                await process_high_priority_task(high_msg)

        async def consume_low_priority():
            async for low_msg in low_consumer:
                await process_low_priority_task(low_msg)

        await asyncio.gather(consume(), consume_low_priority())

    finally:
        await high_consumer.stop()
        await low_consumer.stop()
