import asyncio
import json

from aiokafka import AIOKafkaConsumer

from logger_config import logger
from src.config import settings
from src.tasks.processing import process_task


async def consume_tasks():
    """
    Consume tasks from Kafka queues and process them asynchronously.

    This function creates two Kafka consumers for high and low priority queues,
    starts consuming messages from the queues,
    and processes the tasks asynchronously.

    Raises:
        Exception: If there's an error in consuming or processing the tasks.
    """
    high_consumer = AIOKafkaConsumer(
        "high_priority_queue",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    low_consumer = AIOKafkaConsumer(
        "low_priority_queue",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    await high_consumer.start()
    await low_consumer.start()

    try:

        async def process_high_priority_task(high_msg):
            """
            Process a high priority task asynchronously.

            Args:
                high_msg: Kafka message containing the task data.
            """
            task_data = json.loads(high_msg.value.decode())
            await process_task(task_data)
            logger.info("Task was sent to high priority")

        async def process_low_priority_task(low_msg):
            """
            Process a low priority task asynchronously.

            Args:
                low_msg: Kafka message containing the task data.
            """
            task_data = json.loads(low_msg.value.decode())
            await asyncio.sleep(5)
            await process_task(task_data)
            logger.info("Task was sent to low priority")

        async def consume():
            """Consume messages from the high priority queue."""
            async for high_msg in high_consumer:
                await process_high_priority_task(high_msg)

        async def consume_low_priority():
            """Consume messages from the low priority queue."""
            async for low_msg in low_consumer:
                await process_low_priority_task(low_msg)

        await asyncio.gather(consume(), consume_low_priority())

    finally:
        await high_consumer.stop()
        await low_consumer.stop()
