from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .postgres_repo import PostgresRepo
from .database import get_db


async def get_postgres_repo() -> AsyncGenerator[PostgresRepo, None]:
    """
    Dependency that provides a PostgresRepo instance with a database session.
    """
    async for session in get_db():
        yield PostgresRepo(db_session=session)