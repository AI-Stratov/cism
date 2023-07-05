from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, MetaData, Enum
from sqlalchemy.orm import declarative_base

from src.tasks.schemas import TaskStatus, TaskPriority

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Task(Base):
    __tablename__ = "tasks"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(TaskStatus))
    priority = Column(Enum(TaskPriority))
    created_at = Column(DateTime, default=datetime.now)
    processed_at = Column(DateTime, default=None)
    completed_at = Column(DateTime, default=None)
