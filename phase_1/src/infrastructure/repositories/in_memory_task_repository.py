"""
In-memory implementation of Task repository.
"""
import asyncio
from typing import Dict, List, Optional
from src.domain.interfaces.task_repository import TaskRepository
from src.domain.models.task import Task


class InMemoryTaskRepository(TaskRepository):
    """
    In-memory implementation of Task repository.
    """
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._next_id = 1

    async def create(self, task: Task) -> Task:
        """Create a new task."""
        self._tasks[task.id] = task
        return task

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        return self._tasks.get(task_id)

    async def list(self, status: Optional[str] = None) -> List[Task]:
        """List tasks with optional status filter."""
        tasks = list(self._tasks.values())
        
        if status == "completed":
            tasks = [task for task in tasks if task.completed]
        elif status == "incomplete":
            tasks = [task for task in tasks if not task.completed]
        # If status is "all" or None, return all tasks
        
        return tasks

    async def update(self, task_id: str, task: Task) -> Optional[Task]:
        """Update an existing task."""
        if task_id in self._tasks:
            self._tasks[task_id] = task
            return task
        return None

    async def delete(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    async def toggle_completion(self, task_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self._tasks.get(task_id)
        if task:
            task.completed = not task.completed
            from datetime import datetime
            task.updated_at = datetime.utcnow().isoformat() + "Z"  # Update timestamp
            return task
        return None