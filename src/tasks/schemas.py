from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROCESS = "in_process"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low_priority_queue"
    HIGH = "high_priority_queue"


class TaskSchema(BaseModel):
    id: int
    priority: int
    status: TaskStatus
    created_at: datetime
    processed_at: datetime = None
    completed_at: datetime = None


class TaskResponse(BaseModel):
    id: int
    status: TaskStatus


class FullTaskResponse(TaskResponse):
    execution_time: float
