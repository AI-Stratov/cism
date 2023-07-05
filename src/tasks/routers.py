import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Task
from src.tasks.producer import produce_task_hq, produce_task_lq
from src.tasks.schemas import (FullTaskResponse, TaskPriority, TaskResponse,
                               TaskStatus)

router = APIRouter()


def task_to_dict(task: Task) -> dict:
    return {
        "id": task.id,
        "priority": task.priority,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
        "processed_at": task.processed_at,
        "completed_at": task.completed_at,
    }


@router.post(
    "/create/",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Create a new task",
    description="Create a new task with the given priority.",
)
async def create_task(priority: TaskPriority, db: Session = Depends(get_db)):
    """
    Create a new task.

    Args:
        - priority: Priority of the task (LOW or HIGH).

    Returns:
        - TaskResponse: Response containing the
        ID and status of the created task.
    """
    task = Task(
        status=TaskStatus.CREATED,
        priority=priority,
        created_at=datetime.now(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    task_dict = task_to_dict(task)
    if priority == TaskPriority.LOW:
        asyncio.create_task(produce_task_lq(task_dict))
    elif priority == TaskPriority.HIGH:
        asyncio.create_task(produce_task_hq(task_dict))

    task_response = TaskResponse(
        id=task.id,
        status=task.status,
    )

    return task_response


@router.get(
    "/status/{task_id}/",
    response_model=FullTaskResponse,
    tags=["Tasks"],
    summary="Get the status of a task",
    description="Get the status of a task by its ID.",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get the status of a task by its ID.

    Args:
        - task_id: ID of the task.

    Returns:
        - FullTaskResponse: Response containing the ID, status,
        and execution time of the task.
    """
    task = db.query(Task).get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.COMPLETED:
        execution_time = (task.completed_at - task.created_at).total_seconds()
    else:
        execution_time = (datetime.now() - task.created_at).total_seconds()

    task_response = FullTaskResponse(
        id=task.id,
        status=task.status,
        execution_time=execution_time,
    )
    return task_response
