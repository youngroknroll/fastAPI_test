from typing import Optional

from sqlmodel import Session, select

from app.models.article_model import Article


class ArticleRepository:

    def __init__(self, session: Session):
        self._session = session

    def get_by_slug(self, slug: str) -> Optional[Article]:
        statement = select(Article).where(Article.slug == slug)
        return self._session.exec(statement).first()

    def get_all(self, author_id: int = None, article_ids: list[int] = None) -> list[Article]:
        statement = select(Article)
        if author_id is not None:
            statement = statement.where(Article.author_id == author_id)
        if article_ids is not None:
            statement = statement.where(Article.id.in_(article_ids))
        return list(self._session.exec(statement).all())

    def create(self, slug: str, title: str, description: str, body: str, author_id: int) -> Article:
        article = Article(
            slug=slug, title=title, description=description, body=body, author_id=author_id
        )
        self._session.add(article)
        self._session.commit()
        self._session.refresh(article)
        return article

    def update(self, article: Article, **kwargs) -> Article:
        for key, value in kwargs.items():
            if value is not None:
                setattr(article, key, value)
        self._session.add(article)
        self._session.commit()
        self._session.refresh(article)
        return article

    def delete(self, article: Article) -> None:
        self._session.delete(article)
        self._session.commit()
