import pytest
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture
def session():
    # 각 테스트마다 새로운 in-memory DB 세션을 생성
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session