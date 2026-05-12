from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import engine 
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# test database — separate from real one
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine)

# override get_db to use test database
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
    response = client.post("/register", 
                           json= {
                               "username" : "testuser",
                               "email" : "test@gmail.com",
                               "password" : "test123"
                           }
)
    assert response.status_code == 201

def test_login():
    response = client.post("/login", data={
        "username" : "testuser",
        "password" : "test123"
    })
    assert response.status_code == 200

