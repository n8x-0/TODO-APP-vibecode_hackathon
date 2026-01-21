from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from src.auth.jwt import verify_token
from src.infra.postgres_repo import PostgresRepo
from src.infra.repo_factory import get_postgres_repo
from typing import Optional


security = HTTPBearer()


async def get_current_user(
    request: Request,
    repo: PostgresRepo = Depends(get_postgres_repo)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = verify_token(token, credentials_exception)

    # Get user from repository
    user = await repo.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user