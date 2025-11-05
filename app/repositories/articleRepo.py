from typing import Optional
from sqlmodel import SQLModel, Field, Session, select

class Article(SQLModel, table=True):
    __tablename__ = "articles"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str

class ArticleRepo:
    def __init__(self, session: Session):
        self.session = session

    def list(self):
        statement = select(Article)
        return self.session.exec(statement).all()

    def get(self, article_id: int) -> Optional[Article]:
        return self.session.get(Article, article_id)

    def create(self, title: str, author: str) -> Article:
        article = Article(title=title, author=author)
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article