import asyncio
import logging
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Task
from src.tasks.schemas import TaskStatus
from logger_config import logger



async def process_task(task_data: dict):
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
    while True:
        await asyncio.sleep(60)
        db = next(get_db())
        delete_old_messages(db)


def delete_old_messages(db: Session):
    threshold_datetime = datetime.now() - timedelta(hours=1)
    db.query(Task).filter(Task.created_at < threshold_datetime).delete()
    db.commit()
