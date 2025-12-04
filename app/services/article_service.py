"""Article Service - Business logic for article operations"""

import re
from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.models.article_model import Article
from app.models.user_model import User
from app.repositories.article_repository import ArticleRepository
from app.repositories.user_repository import UserRepository


def slugify(title: str) -> str:
    """Convert title to slug"""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = slug.strip("-")
    return slug


class ArticleService:
    """Article business logic"""

    def __init__(self, session: Session):
        self.session = session
        self.repo = ArticleRepository(session)
        self.user_repo = UserRepository(session)

    def create_article(
        self, title: str, description: str, body: str, author: User
    ) -> dict:
        """
        Create a new article

        Returns:
            dict: Article data
        """
        slug = slugify(title)

        article = self.repo.create(
            slug=slug,
            title=title,
            description=description,
            body=body,
            author_id=author.id,
        )

        return self._format_article_response(article, author)

    def get_article_by_slug(self, slug: str) -> dict:
        """
        Get article by slug

        Returns:
            dict: Article data

        Raises:
            HTTPException: 404 if article not found
        """
        article = self.repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        author = self.user_repo.get_by_id(article.author_id)

        return self._format_article_response(article, author)

    def get_articles(self) -> dict:
        """
        Get all articles

        Returns:
            dict: Articles list with count
        """
        articles = self.repo.get_all()

        articles_data = []
        for article in articles:
            author = self.user_repo.get_by_id(article.author_id)
            articles_data.append(self._format_article_response(article, author)["article"])

        return {"articles": articles_data, "articlesCount": len(articles_data)}

    def _format_article_response(self, article: Article, author: User) -> dict:
        """Format article response"""
        return {
            "article": {
                "slug": article.slug,
                "title": article.title,
                "description": article.description,
                "body": article.body,
                "createdAt": article.created_at.isoformat() + "Z",
                "updatedAt": article.updated_at.isoformat() + "Z",
                "author": {
                    "username": author.username,
                    "bio": author.bio,
                    "image": author.image,
                    "following": False,
                },
            }
        }

