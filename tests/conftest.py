import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture
def session():
    """각 테스트마다 새로운 in-memory DB 세션 생성"""
    # check_same_thread=False 추가 - SQLite 스레드 체크 비활성화
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},  # ← 핵심!
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
