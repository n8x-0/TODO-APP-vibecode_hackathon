"""
Repository interface for Task entities.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.task import Task


class TaskRepository(ABC):
    """
    Abstract interface for Task repository operations.
    """

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        pass

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        pass

    @abstractmethod
    async def list(self, status: Optional[str] = None) -> List[Task]:
        """List tasks with optional status filter."""
        pass

    @abstractmethod
    async def update(self, task_id: str, task: Task) -> Optional[Task]:
        """Update an existing task."""
        pass

    @abstractmethod
    async def delete(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        pass

    @abstractmethod
    async def toggle_completion(self, task_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        pass