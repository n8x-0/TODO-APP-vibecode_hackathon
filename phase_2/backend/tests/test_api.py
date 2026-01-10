import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_signup():
    # Test signup with valid data
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    
    # Test signup with existing email
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 409

def test_login():
    # Test login with valid credentials
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    
    # Test login with invalid credentials
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400

def test_logout():
    # First, login to get a session
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200
    
    # Then logout
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}

def test_get_current_user():
    # First, login to get a session
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200
    
    # Then get current user
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "email" in response.json()
    assert "created_at" in response.json()

def test_get_current_user_unauthenticated():
    # Test getting current user without authentication
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401