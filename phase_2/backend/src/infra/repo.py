from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.user import UserCreate, UserUpdate, User
from src.domain.models.task import TaskCreate, TaskUpdate, Task
import uuid
from datetime import datetime
from src.auth.utils import get_password_hash

class TodoRepository(ABC):

    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        pass

    @abstractmethod
    async def create_task(self, user_id: str, task: TaskCreate) -> Task:
        pass

    @abstractmethod
    async def get_tasks(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        pass

    @abstractmethod
    async def get_task(self, user_id: str, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    async def update_task(self, user_id: str, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        pass

    @abstractmethod
    async def delete_task(self, user_id: str, task_id: str) -> bool:
        pass

    @abstractmethod
    async def toggle_task_completion(self, user_id: str, task_id: str) -> Optional[Task]:
        pass


class InMemoryRepo(TodoRepository):
    def __init__(self):
        self.users = {}
        self.tasks = {}

    async def create_user(self, user: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        # Create user with basic information
        db_user = User(
            id=user_id,
            email=user.email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
        # Store the user
        self.users[user_id] = db_user
        # Store the hashed password separately
        if not hasattr(self, 'passwords'):
            self.passwords = {}
        self.passwords[user_id] = get_password_hash(user.password)  # Hash the password before storing
        return db_user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        if user_id in self.users:
            user = self.users[user_id]
            if user_update.email is not None:
                user.email = user_update.email
            user.updated_at = datetime.utcnow()
            return user
        return None

    async def create_task(self, user_id: str, task: TaskCreate) -> Task:
        task_id = str(uuid.uuid4())
        db_task = Task(
            id=task_id,
            user_id=user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_at=task.due_at,
            priority=task.priority,
            tags=task.tags or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.tasks[task_id] = db_task
        return db_task

    async def get_tasks(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        user_tasks = [task for task in self.tasks.values() if task.user_id == user_id]

        if status == "completed":
            user_tasks = [task for task in user_tasks if task.completed]
        elif status == "incomplete":
            user_tasks = [task for task in user_tasks if not task.completed]
        # If status is "all" or None, return all tasks for the user

        return user_tasks

    async def get_task(self, user_id: str, task_id: str) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if task and task.user_id == user_id:
            return task
        return None

    async def update_task(self, user_id: str, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        if task_id in self.tasks and self.tasks[task_id].user_id == user_id:
            task = self.tasks[task_id]
            for field, value in task_update.dict(exclude_unset=True).items():
                setattr(task, field, value)
            task.updated_at = datetime.utcnow()
            return task
        return None

    async def delete_task(self, user_id: str, task_id: str) -> bool:
        if task_id in self.tasks and self.tasks[task_id].user_id == user_id:
            del self.tasks[task_id]
            return True
        return False

    async def toggle_task_completion(self, user_id: str, task_id: str) -> Optional[Task]:
        if task_id in self.tasks and self.tasks[task_id].user_id == user_id:
            task = self.tasks[task_id]
            task.completed = not task.completed
            task.updated_at = datetime.utcnow()
            return task
        return None