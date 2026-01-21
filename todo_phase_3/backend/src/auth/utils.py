from passlib.context import CryptContext
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes to comply with bcrypt limitations
    # This is a bcrypt limitation - passwords longer than 72 bytes will be truncated
    pwd_context.default_scheme()
    return pwd_context.hash(password)