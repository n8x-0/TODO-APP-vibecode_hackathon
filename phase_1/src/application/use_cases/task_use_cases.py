"""
Task use cases implementing business logic.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from src.domain.interfaces.task_repository import TaskRepository
from src.domain.models.task import Task


def generate_task_id() -> str:
    """Generate a unique task ID using epoch milliseconds with uniqueness suffix."""
    epoch_ms = int(datetime.now().timestamp() * 1000)
    unique_suffix = str(uuid.uuid4())[:8]
    return f"{epoch_ms}-{unique_suffix}"


class TaskUseCases:
    """
    Task use cases implementing business logic.
    """
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        due_at: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create a new task with validation."""
        # Validate title
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required and cannot be empty.")
        if len(title) > 200:
            raise ValueError("Title cannot exceed 200 characters.")
        
        # Validate priority if provided
        if priority and priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of 'low', 'medium', or 'high'.")
        
        # Normalize tags if provided
        normalized_tags = []
        if tags:
            for tag in tags:
                if tag and tag.strip():
                    normalized_tag = tag.strip()
                    if normalized_tag not in normalized_tags:
                        normalized_tags.append(normalized_tag)
        
        task_id = generate_task_id()
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description,
            due_at=due_at,
            priority=priority,
            tags=normalized_tags
        )
        
        return await self.task_repository.create(task)

    async def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        return await self.task_repository.get_by_id(task_id)

    async def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """List tasks with optional status filter."""
        return await self.task_repository.list(status)

    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_at: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Task]:
        """Update an existing task."""
        existing_task = await self.task_repository.get_by_id(task_id)
        if not existing_task:
            return None

        # Validate title if provided
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValueError("Title is required and cannot be empty.")
            if len(title) > 200:
                raise ValueError("Title cannot exceed 200 characters.")
        
        # Validate priority if provided
        if priority and priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of 'low', 'medium', or 'high'.")

        # Update fields if provided
        if title is not None:
            existing_task.title = title.strip()
        if description is not None:
            existing_task.description = description
        if due_at is not None:
            existing_task.due_at = due_at
        if priority is not None:
            existing_task.priority = priority
        if tags is not None:
            # Normalize tags
            normalized_tags = []
            for tag in tags:
                if tag and tag.strip():
                    normalized_tag = tag.strip()
                    if normalized_tag not in normalized_tags:
                        normalized_tags.append(normalized_tag)
            existing_task.tags = normalized_tags

        # Update timestamp
        from datetime import datetime
        existing_task.updated_at = datetime.utcnow().isoformat() + "Z"

        return await self.task_repository.update(task_id, existing_task)

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        return await self.task_repository.delete(task_id)

    async def toggle_task_completion(self, task_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        return await self.task_repository.toggle_completion(task_id)