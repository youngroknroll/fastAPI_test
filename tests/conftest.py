"""Test configuration"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.main import app

# Import all models to register them with SQLModel (order matters for FK resolution)
from app.models.user_model import User  # noqa: F401
from app.models.follow_model import Follow  # noqa: F401
from app.models.article_model import Article  # noqa: F401
from app.models.tag_model import ArticleTag, Tag  # noqa: F401
from app.models.favorite_model import Favorite  # noqa: F401
from app.models.comment_model import Comment  # noqa: F401


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


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with test database"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user1_token")
def token_fixture(client):
        # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    return token

@pytest.fixture(name="user2_token")
def token_fixture(client):
    # 유저2 등록
    user2_payload = {
        "user": {"email": "user2@example.com", "password": "password123", "username": "user2"}
    }
    user2_response = client.post("/users", json=user2_payload)
    user2_token = user2_response.json()["user"]["token"]
    return user2_token