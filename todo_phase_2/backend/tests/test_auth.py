import pytest
from src.auth.utils import get_password_hash, verify_password
from src.auth.jwt import create_access_token, decode_access_token
from datetime import timedelta
import jwt


def test_get_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert len(hashed_password) > 0
    assert hashed_password != password


def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    
    # Verify correct password
    assert verify_password(password, hashed_password) == True
    
    # Verify incorrect password
    assert verify_password("wrongpassword", hashed_password) == False


def test_create_access_token():
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data=data, expires_delta=expires_delta)
    
    assert token is not None
    assert len(token) > 0
    
    # Decode and verify token
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "test@example.com"


def test_decode_access_token():
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data=data, expires_delta=expires_delta)
    
    # Decode token
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "test@example.com"
    
    # Test expired token
    expired_token = create_access_token(data=data, expires_delta=timedelta(seconds=-1))
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(expired_token)


def test_decode_invalid_token():
    # Test invalid token
    with pytest.raises(jwt.JWTError):
        decode_access_token("invalid.token")