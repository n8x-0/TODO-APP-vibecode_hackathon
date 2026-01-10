from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, and_
from src.domain.models.user import UserCreate, UserUpdate, User
from src.domain.models.task import TaskCreate, TaskUpdate, Task
from .db_models.models import User as DBUser, Task as DBTask
from src.auth.utils import get_password_hash
import uuid
from datetime import datetime


class PostgresRepo:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, user: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user.password)  # Hash the password before storing
        db_user = DBUser(
            id=user_id,
            email=user.email,
            hashed_password=hashed_password
        )
        self.db_session.add(db_user)
        await self.db_session.commit()
        await self.db_session.refresh(db_user)

        # Return the Pydantic model
        return User(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            is_active=db_user.is_active
        )

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db_session.execute(
            select(DBUser).filter(DBUser.email == email)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
                is_active=db_user.is_active
            )
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        result = await self.db_session.execute(
            select(DBUser).filter(DBUser.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
                is_active=db_user.is_active
            )
        return None

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        stmt = (
            update(DBUser)
            .where(DBUser.id == user_id)
            .values(**user_update.dict(exclude_unset=True, exclude_defaults=True))
            .returning(DBUser)
        )
        result = await self.db_session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        if db_user:
            await self.db_session.commit()
            await self.db_session.refresh(db_user)
            return User(
                id=db_user.id,
                email=db_user.email,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
                is_active=db_user.is_active
            )
        return None

    async def create_task(self, user_id: str, task: TaskCreate) -> Task:
        task_id = str(uuid.uuid4())
        db_task = DBTask(
            id=task_id,
            user_id=user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_at=task.due_at,
            priority=task.priority,
            tags=task.tags or []
        )
        self.db_session.add(db_task)
        await self.db_session.commit()
        await self.db_session.refresh(db_task)
        
        return Task(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            due_at=db_task.due_at,
            priority=db_task.priority,
            tags=db_task.tags,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )

    async def get_tasks(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        query = select(DBTask).filter(DBTask.user_id == user_id)
        
        if status == "completed":
            query = query.filter(DBTask.completed == True)
        elif status == "incomplete":
            query = query.filter(DBTask.completed == False)
        
        result = await self.db_session.execute(query)
        db_tasks = result.scalars().all()
        
        return [
            Task(
                id=db_task.id,
                user_id=db_task.user_id,
                title=db_task.title,
                description=db_task.description,
                completed=db_task.completed,
                due_at=db_task.due_at,
                priority=db_task.priority,
                tags=db_task.tags,
                created_at=db_task.created_at,
                updated_at=db_task.updated_at
            )
            for db_task in db_tasks
        ]

    async def get_task(self, user_id: str, task_id: str) -> Optional[Task]:
        result = await self.db_session.execute(
            select(DBTask).filter(
                and_(DBTask.id == task_id, DBTask.user_id == user_id)
            )
        )
        db_task = result.scalar_one_or_none()
        if db_task:
            return Task(
                id=db_task.id,
                user_id=db_task.user_id,
                title=db_task.title,
                description=db_task.description,
                completed=db_task.completed,
                due_at=db_task.due_at,
                priority=db_task.priority,
                tags=db_task.tags,
                created_at=db_task.created_at,
                updated_at=db_task.updated_at
            )
        return None

    async def update_task(self, user_id: str, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        # Get current task to ensure it belongs to the user
        current_task = await self.get_task(user_id, task_id)
        if not current_task:
            return None
            
        # Update the task
        update_data = task_update.dict(exclude_unset=True)
        stmt = (
            update(DBTask)
            .where(DBTask.id == task_id)
            .values(**update_data)
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        
        # Return updated task
        return await self.get_task(user_id, task_id)

    async def delete_task(self, user_id: str, task_id: str) -> bool:
        result = await self.db_session.execute(
            delete(DBTask).filter(
                and_(DBTask.id == task_id, DBTask.user_id == user_id)
            )
        )
        await self.db_session.commit()
        return result.rowcount > 0

    async def toggle_task_completion(self, user_id: str, task_id: str) -> Optional[Task]:
        # Get current task to ensure it belongs to the user
        current_task = await self.get_task(user_id, task_id)
        if not current_task:
            return None
            
        # Toggle completion status
        new_completion_status = not current_task.completed
        stmt = (
            update(DBTask)
            .where(DBTask.id == task_id)
            .values(completed=new_completion_status)
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        
        # Return updated task
        return await self.get_task(user_id, task_id)