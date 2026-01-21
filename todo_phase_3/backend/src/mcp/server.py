"""
MCP Server implementation using Official MCP SDK (FastMCP).
Exposes todo task management tools for Agents via MCP HTTP endpoints.
"""

import json
import logging
from datetime import datetime
from typing import Optional
from uuid import UUID
from contextlib import asynccontextmanager

from mcp.server import FastMCP

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import select

from src.config import get_settings
from src.infra.db_models.models import Task

logger = logging.getLogger(__name__)

# ✅ Initialize FastMCP server
mcp = FastMCP(name="todo-mcp-server")

_async_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _async_session_factory
    if _async_session_factory is None:
        settings = get_settings()
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
        )
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


@asynccontextmanager
async def get_db_session():
    factory = get_session_factory()
    async with factory() as session:
        yield session


async def _find_task_by_title(session: AsyncSession, user_id: str, task_title: str) -> list[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .where(Task.title.ilike(f"%{task_title}%"))
    )
    result = await session.execute(statement)
    matches = list(result.scalars().all())
    if matches:
        return matches

    words = [w.strip() for w in task_title.split() if len(w.strip()) >= 3]
    for word in words:
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.title.ilike(f"%{word}%"))
        )
        result = await session.execute(statement)
        word_matches = list(result.scalars().all())
        if word_matches:
            return word_matches

    return []


# =============================================================================
# MCP Tools
# =============================================================================

@mcp.tool()
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> str:
    logger.info(f"MCP add_task called: user_id={user_id}, title={title}")

    async with get_db_session() as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return json.dumps({
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
            }
        })


@mcp.tool()
async def list_tasks(user_id: str, status: str = "all", limit: int = 50) -> str:
    logger.info(f"MCP list_tasks called: user_id={user_id}, status={status}")

    async with get_db_session() as session:
        statement = select(Task).where(Task.user_id == user_id)

        if status == "completed":
            statement = statement.where(Task.completed.is_(True))
        elif status == "incomplete":
            statement = statement.where(Task.completed.is_(False))

        statement = statement.order_by(Task.created_at.desc()).limit(limit)

        result = await session.execute(statement)
        tasks = result.scalars().all()

        return json.dumps({
            "success": True,
            "tasks": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "due_at": t.due_at.isoformat() if t.due_at else None
                }
                for t in tasks
            ],
            "count": len(tasks)
        })


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: Optional[str] = None,
    task_title: Optional[str] = None,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None
) -> str:
    logger.info(f"MCP update_task called: user_id={user_id}, task_id={task_id}, task_title={task_title}")

    async with get_db_session() as session:
        task = None

        if task_id:
            try:
                uuid = UUID(task_id)
            except ValueError:
                return json.dumps({"success": False, "error": "Invalid task ID format"})

            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

        elif task_title:
            matches = await _find_task_by_title(session, user_id, task_title)
            if len(matches) == 0:
                return json.dumps({"success": False, "error": f"No task found matching '{task_title}'"})
            if len(matches) > 1:
                return json.dumps({
                    "success": False,
                    "error": "Multiple tasks match that title",
                    "matches": [{"id": str(t.id), "title": t.title} for t in matches],
                })
            task = matches[0]

        if task is None:
            return json.dumps({"success": False, "error": "Task not found. Provide task_id or task_title."})

        if new_title:
            task.title = new_title
        if new_description is not None:
            task.description = new_description

        task.updated_at = datetime.utcnow()
        await session.commit()

        return json.dumps({
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
        })


@mcp.tool()
async def complete_task_toggle(user_id: str, task_id: Optional[str] = None, task_title: Optional[str] = None) -> str:
    logger.info(f"MCP complete_task_toggle called: user_id={user_id}, task_id={task_id}, task_title={task_title}")

    async with get_db_session() as session:
        task = None

        if task_id:
            try:
                uuid = UUID(task_id)
            except ValueError:
                return json.dumps({"success": False, "error": "Invalid task ID format"})

            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

        elif task_title:
            matches = await _find_task_by_title(session, user_id, task_title)
            if len(matches) == 0:
                return json.dumps({"success": False, "error": f"No task found matching '{task_title}'"})
            if len(matches) > 1:
                return json.dumps({
                    "success": False,
                    "error": "Multiple tasks match that title",
                    "matches": [{"id": str(t.id), "title": t.title} for t in matches],
                })
            task = matches[0]

        if task is None:
            return json.dumps({"success": False, "error": "Task not found. Provide task_id or task_title."})

        task.completed = not task.completed
        task.completed_at = datetime.utcnow() if task.completed else None
        task.updated_at = datetime.utcnow()
        await session.commit()

        action = "completed" if task.completed else "unmarked"
        return json.dumps({
            "success": True,
            "message": f"Task '{task.title}' has been {action}.",
            "task": {
                "id": str(task.id),
                "title": task.title,
                "completed": task.completed,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
        })


@mcp.tool()
async def delete_task(user_id: str, task_id: Optional[str] = None, task_title: Optional[str] = None) -> str:
    logger.info(f"MCP delete_task called: user_id={user_id}, task_id={task_id}, task_title={task_title}")

    async with get_db_session() as session:
        task = None

        if task_id:
            try:
                uuid = UUID(task_id)
            except ValueError:
                return json.dumps({"success": False, "error": "Invalid task ID format"})

            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

        elif task_title:
            matches = await _find_task_by_title(session, user_id, task_title)
            if len(matches) == 0:
                return json.dumps({"success": False, "error": f"No task found matching '{task_title}'"})
            if len(matches) > 1:
                return json.dumps({
                    "success": False,
                    "error": "Multiple tasks match that title",
                    "matches": [{"id": str(t.id), "title": t.title} for t in matches],
                })
            task = matches[0]

        if task is None:
            return json.dumps({"success": False, "error": "Task not found. Provide task_id or task_title."})

        title_deleted = task.title
        await session.delete(task)
        await session.commit()

        return json.dumps({"success": True, "message": f"Task '{title_deleted}' has been deleted."})


def get_mcp_server() -> FastMCP:
    return mcp
