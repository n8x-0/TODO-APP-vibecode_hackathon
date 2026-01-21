from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_at: Optional[datetime] = None
    priority: Optional[str] = "medium"  # low, medium, high
    tags: Optional[List[str]] = []


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_at: Optional[datetime] = None
    priority: Optional[str] = None  # low, medium, high
    tags: Optional[List[str]] = None


class Task(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True