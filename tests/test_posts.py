import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Isolated in-memory SQLite test database with StaticPool
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_get_posts():
    response = client.get("/posts")
    assert response.status_code == 200

def test_get_post():
    response = client.get("/posts/9999")
    assert response.status_code == 404

def test_create_post():
    response = client.post("/posts")
    assert response.status_code == 401

def test_update_post():
    response = client.put("/posts/9999")
    assert response.status_code == 401

def test_delete_post():
    response = client.delete("/posts/9999")
    assert response.status_code == 401

def test_register_user():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "test123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@gmail.com"
    assert "id" in data

def test_login():
    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "test123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
