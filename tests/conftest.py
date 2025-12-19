"""Test configuration"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.main import app

# DB
@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# client session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with test database"""
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    
    try:
        with TestClient(app) as client:
            yield client
    finally:            
        app.dependency_overrides.clear()


# user payload
@pytest.fixture(name="user1_payload")
def user1_payload(client):
    # user1 등록
    user1_payload = {
        "user": {"email": "user1@example.com", "password": "password123", "username": "user1"}
    }
    #토큰
    response = client.post("/users", json=user1_payload)
    token = response.json()["user"]["token"]
    return token

@pytest.fixture(name="user2_payload")
def user2_payload(client):
    # 유저2 등록
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    #토큰
    response  = client.post("/users", json=user2_payload)
    token = response.json()["user"]["token"]
    return token

@pytest.fixture(name="user1_header")
def user1_header(user1_payload):
    headers = {"Authorization": f"Token {user1_payload}"}
    return headers
    
@pytest.fixture(name="user2_header")
def user2_header(user2_payload):
    headers = {"Authorization": f"Token {user2_payload}"}
    return headers
    
    
#article payload
@pytest.fixture(name="article_payload")
def article_payload():
    payload = {
        "article": {"title": "Test Article", "description": "Test Desc", "body": "Test Body"}
    }
    return payload

#article API
class ArticleAPI:
    def __init__(self, client):
        self._client = client

    def create(self, payload, headers=None):
        return self._client.post("/articles", json=payload, headers=headers)

    def delete(self, slug, headers=None):
        return self._client.delete(f"/articles/{slug}", headers=headers)

    def get(self, slug, headers=None):
        return self._client.get(f"/articles/{slug}", headers=headers)
    
@pytest.fixture
def article_api(client):
    return ArticleAPI(client)