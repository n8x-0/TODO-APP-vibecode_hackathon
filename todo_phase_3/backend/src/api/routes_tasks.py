from fastapi import APIRouter, Depends, HTTPException, status, Response
from src.domain.models.task import TaskCreate, TaskUpdate, Task
from src.api.deps import get_current_user
from src.infra.postgres_repo import PostgresRepo
from src.infra.repo_factory import get_postgres_repo
from typing import List, Optional


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task])
async def get_tasks(
    status_param: Optional[str] = None,
    current_user = Depends(get_current_user),
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate status parameter
    if status_param and status_param not in ['all', 'completed', 'incomplete']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status parameter. Must be 'all', 'completed', or 'incomplete'"
        )

    tasks = await repo.get_tasks(current_user.id, status_param)
    return tasks


@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate,
    current_user = Depends(get_current_user),
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate task data
    if not task.title or len(task.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title is required"
        )

    # Create the task
    db_task = await repo.create_task(current_user.id, task)
    return db_task


@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user = Depends(get_current_user),
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate that the task exists and belongs to the user
    existing_task = await repo.get_task(current_user.id, task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Validate task data
    if task_update.title is not None and len(task_update.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    # Update the task
    db_task = await repo.update_task(current_user.id, task_id, task_update)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.post("/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(
    task_id: str,
    current_user = Depends(get_current_user),
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate that the task exists and belongs to the user
    existing_task = await repo.get_task(current_user.id, task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the task completion status
    db_task = await repo.toggle_task_completion(current_user.id, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user = Depends(get_current_user),
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate that the task exists and belongs to the user
    existing_task = await repo.get_task(current_user.id, task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task
    success = await repo.delete_task(current_user.id, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}