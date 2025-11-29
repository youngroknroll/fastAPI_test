from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends

from app.services.article_service import ArticleService


DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_article_service(session: Session = Depends(get_session)):
    return ArticleService(session)
