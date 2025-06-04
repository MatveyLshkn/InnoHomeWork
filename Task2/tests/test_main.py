from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database import Base, get_db
from app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "phone": "123-456-7890",
            "website": "test.com",
            "address": {
                "street": "Test Street",
                "suite": "Test Suite",
                "city": "Test City",
                "zipcode": "12345",
                "geo": {
                    "lat": "0",
                    "lng": "0"
                }
            },
            "company": {
                "name": "Test Company",
                "catchPhrase": "Test Phrase",
                "bs": "Test BS"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_users():
    # Create a test user first
    test_create_user()
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == "testuser"

def test_get_user():
    # Create a test user first
    test_create_user()
    
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_update_user():
    # Create a test user first
    test_create_user()
    
    response = client.put(
        "/users/1",
        json={
            "name": "Updated User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "phone": "123-456-7890",
            "website": "test.com",
            "address": {
                "street": "Test Street",
                "suite": "Test Suite",
                "city": "Test City",
                "zipcode": "12345",
                "geo": {
                    "lat": "0",
                    "lng": "0"
                }
            },
            "company": {
                "name": "Test Company",
                "catchPhrase": "Test Phrase",
                "bs": "Test BS"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User"

def test_delete_user():
    # Create a test user first
    test_create_user()
    
    response = client.delete("/users/1")
    assert response.status_code == 200
    
    # Verify user is deleted
    response = client.get("/users/1")
    assert response.status_code == 404 