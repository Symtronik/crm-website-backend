import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.src.common.dependencies import get_db

from app.src.module.users.models import User, DBBase
from app.src.module.users.crud import get_user_by_username, get_password_hash, authenticate_user
os.environ["SECRET_KEY"] = "your_secret_key"
os.environ["HASHING_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["POSTGRES_DATABASE_URL"] = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DBBase.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Utility function to add a test user
def add_test_user(db):
    fake_user = User(
        username="jula",
        hashed_password=get_password_hash("jula"),
        surname="Doe",
        name="John",
        email="jula@example.com",
        is_active=True
    )
    db.add(fake_user)
    db.commit()
    db.refresh(fake_user)
    return fake_user

# Test for the get_user function
def test_get_user():
    db = next(override_get_db())
    add_test_user(db)
    user = get_user_by_username(db, username="jula")
    assert user
    assert user.username == "jula"

# Test for the authenticate_user function
def test_authenticate_user():
    db = next(override_get_db())
    add_test_user(db)
    authenticated_user = authenticate_user(db, "jula", "jula")
    assert authenticated_user
    assert authenticated_user.username == "jula"

# Test for the /token endpoint
def test_login_for_access_token():
    db = next(override_get_db())
    add_test_user(db)
    response = client.post(
        "/token",
        data={"username": "jula", "password": "jula"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
