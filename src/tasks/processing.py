import asyncio
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from logger_config import logger
from src.database import get_db
from src.models import Task
from src.tasks.schemas import TaskStatus


async def process_task(task_data: dict):
    """
    Process a task asynchronously.

    This function updates the status of a task to "IN_PROCESS",
    performs the task processing logic, and updates the status to "COMPLETED".

    Args:
        task_data: Task data received from the message queue.
    """
    db = next(get_db())
    task_id = task_data["id"]
    task = db.query(Task).get(task_id)

    if task is None:
        logger.error(f"Task with ID {task_id} not found")
        return

    task.status = TaskStatus.IN_PROCESS
    task.processed_at = datetime.now()
    logger.info(f"Task id:{task.id} status changed to {task.status}")

    db.commit()

    await asyncio.sleep(5)

    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.now()
    logger.info(f"Task id:{task.id} status changed to {task.status}")

    db.commit()


async def periodic_task_deletion():
    """
    Perform periodic deletion of old tasks.

    This function runs in the background and periodically deletes tasks
    that were created more than one hour ago.
    """
    while True:
        await asyncio.sleep(60)
        db = next(get_db())
        delete_old_messages(db)


def delete_old_messages(db: Session):
    """
    Delete old tasks from the database.

    This function deletes tasks from the database that were created
    more than one hour ago.

    Args:
        db: Database session object.
    """
    threshold_datetime = datetime.now() - timedelta(hours=1)
    db.query(Task).filter(Task.created_at < threshold_datetime).delete()
    db.commit()
