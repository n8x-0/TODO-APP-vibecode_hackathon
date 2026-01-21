from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from datetime import timedelta
from src.domain.models.user import UserCreate, User
from src.auth.utils import get_password_hash, verify_password
from src.auth.jwt import create_access_token
from src.infra.postgres_repo import PostgresRepo
from src.infra.repo_factory import get_postgres_repo
from src.api.deps import get_current_user
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
import re


router = APIRouter(prefix="/auth", tags=["auth"])

# Rate limit for signup endpoint (5 attempts per minute)
limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", response_model=User)
@limiter.limit("5/minute")
async def signup(
    user: UserCreate,
    response: Response,
    request: Request = None,
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate email format
    if not user.email or not isinstance(user.email, str) or len(user.email.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required and must be a valid string"
        )

    # Validate email format using regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # # Validate password

    if not user.password or not isinstance(user.password, str) or len(user.password.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required and must be a valid string"
        )

    # Password must be at least 8 characters long
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    # Password must be no more than 72 characters long (bcrypt limitation)
    if len(user.password) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be no more than 72 characters long"
        )

    # Check if user already exists
    existing_user = await repo.get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the user
    db_user = await repo.create_user(user)

    # Create access token with longer expiration for session persistence
    access_token_expires = timedelta(days=7)  # 7 days for session persistence
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    # Set cookie with the token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800,
        path="/",
    )

    return db_user


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    user_credentials: UserCreate,
    response: Response,
    request: Request = None,
    repo: PostgresRepo = Depends(get_postgres_repo)
):

    # Validate password length (bcrypt limitation)
    if len(user_credentials.password) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be no more than 72 characters long"
        )

    # Get user from repo
    user = await repo.get_user_by_email(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    # Get the stored hashed password from the database
    # We need to get the DBUser object to access the hashed_password field
    from sqlalchemy.future import select
    from src.infra.db_models.models import User as DBUser
    result = await repo.db_session.execute(
        select(DBUser).filter(DBUser.email == user_credentials.email)
    )
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    # Create access token with longer expiration for session persistence
    access_token_expires = timedelta(days=7)  # 7 days for session persistence
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Set cookie with the token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800,
        path="/",
    )

    return {"id": user.id, "email": user.email, "created_at": user.created_at}


@router.post("/logout")
async def logout(response: Response):
    # Clear the access token cookie
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",  # Can be "strict", "lax", or "none"
        max_age=0,  # Expire immediately
        domain=None,  # Optional: specify domain if needed
        path="/",  # Path for the cookie
        expires=None,  # Optional: set expiration time
    )
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Validate that the user is authenticated
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user