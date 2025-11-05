from fastapi import FastAPI

from app.repositories.articleRepo import ArticleRepo
from sqlmodel import SQLModel, create_engine, Session

def test_article_repository_crud():
    #given sqlite연결, repo
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url, echo=True)

    #테이블 먼저 만들어야 테스트 안터진다.
    SQLModel.metadata.create_all(engine)

    session = Session(engine)
    repo = ArticleRepo(session)

    #when 새로운 글 작성
    created = repo.create(title="test", author="yeong")

    #then title과 author가 저장되어야함
    assert created.id == 1
    assert created.title == "test"

    # when 전체 조회
    articles = repo.list()
    assert len(articles) == 1

    # when ID 조회
    found = repo.get(created.id)
    assert found.title == "test"

    # when 존재하지 않는 ID 조회
    assert repo.get(999) is None