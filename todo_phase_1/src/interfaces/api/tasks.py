"""
Tasks API endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from domain.models.task import Task
from application.use_cases.task_use_cases import TaskUseCases
from infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository

router = APIRouter()

# Initialize repository and use cases
task_repository = InMemoryTaskRepository()
task_use_cases = TaskUseCases(task_repository)


from typing import List, Optional


class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    due_at: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None


@router.post("/tasks", status_code=201, response_model=Task)
async def create_task(request: TaskCreateRequest):
    """Create a new task."""
    try:
        return await task_use_cases.create_task(
            title=request.title,
            description=request.description,
            due_at=request.due_at,
            priority=request.priority,
            tags=request.tags
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: str = Query("all", regex="^(all|completed|incomplete)$")
):
    """List tasks with optional status filter."""
    return await task_use_cases.list_tasks(status=status)


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a single task by ID."""
    task = await task_use_cases.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_at: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None


@router.patch("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, request: TaskUpdateRequest):
    """Update an existing task."""
    task = await task_use_cases.update_task(
        task_id=task_id,
        title=request.title,
        description=request.description,
        due_at=request.due_at,
        priority=request.priority,
        tags=request.tags
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        # Validate any new values
        if request.title is not None:
            if not request.title or len(request.title.strip()) == 0:
                raise ValueError("Title is required and cannot be empty.")
            if len(request.title) > 200:
                raise ValueError("Title cannot exceed 200 characters.")

        if request.priority and request.priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of 'low', 'medium', or 'high'.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    success = await task_use_cases.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted", "id": task_id}


@router.post("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(task_id: str):
    """Toggle task completion status."""
    task = await task_use_cases.toggle_task_completion(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task