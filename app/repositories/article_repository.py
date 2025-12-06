"""Article Repository"""

from typing import Optional

from sqlmodel import Session, select

from app.models.article_model import Article


class ArticleRepository:
    """Article data access layer"""

    def __init__(self, session: Session):
        self.session = session

    def create(
        self, slug: str, title: str, description: str, body: str, author_id: int
    ) -> Article:
        """Create a new article"""
        article = Article(
            slug=slug,
            title=title,
            description=description,
            body=body,
            author_id=author_id,
        )
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def get_by_slug(self, slug: str) -> Optional[Article]:
        """Get article by slug"""
        statement = select(Article).where(Article.slug == slug)
        return self.session.exec(statement).first()

    def get_all(self, author_id: int = None, article_ids: list[int] = None) -> list[Article]:
        """Get all articles with optional filters"""
        statement = select(Article)

        if author_id is not None:
            statement = statement.where(Article.author_id == author_id)

        if article_ids is not None:
            statement = statement.where(Article.id.in_(article_ids))

        return list(self.session.exec(statement).all())

