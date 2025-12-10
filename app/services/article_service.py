"""Article Service - Business logic for article operations"""

import re
from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.models.article_model import Article
from app.models.user_model import User
from app.repositories.article_repository import ArticleRepository
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.tag_repository import TagRepository
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
        self.tag_repo = TagRepository(session)
        self.favorite_repo = FavoriteRepository(session)

    def create_article(
        self, title: str, description: str, body: str, author: User, tag_list: list[str] = None
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

        # Add tags if provided
        if tag_list:
            self.tag_repo.add_tags_to_article(article.id, tag_list)

        return self._format_article_response(article, author, tag_list or [])

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
        tag_list = self.tag_repo.get_tags_for_article(article.id)

        return self._format_article_response(article, author, tag_list)

    def get_articles(self, author: str = None, tag: str = None, favorited: str = None) -> dict:
        """
        Get all articles with optional filters

        Args:
            author: Filter by author username
            tag: Filter by tag name
            favorited: Filter by username who favorited

        Returns:
            dict: Articles list with count
        """
        author_id = None
        if author:
            author_user = self.user_repo.get_by_username(author)
            if author_user:
                author_id = author_user.id
            else:
                # Author not found, return empty list
                return {"articles": [], "articlesCount": 0}

        # Filter by tag
        article_ids = None
        if tag:
            article_ids = self.tag_repo.get_article_ids_by_tag(tag)
            if not article_ids:
                return {"articles": [], "articlesCount": 0}

        # Filter by favorited user
        if favorited:
            favorited_user = self.user_repo.get_by_username(favorited)
            if favorited_user:
                favorited_article_ids = self.favorite_repo.get_article_ids_by_user(favorited_user.id)
                if not favorited_article_ids:
                    return {"articles": [], "articlesCount": 0}
                # Combine with existing article_ids filter
                if article_ids is not None:
                    article_ids = list(set(article_ids) & set(favorited_article_ids))
                else:
                    article_ids = favorited_article_ids
            else:
                return {"articles": [], "articlesCount": 0}

        articles = self.repo.get_all(author_id=author_id, article_ids=article_ids)

        articles_data = []
        for article in articles:
            article_author = self.user_repo.get_by_id(article.author_id)
            tag_list = self.tag_repo.get_tags_for_article(article.id)
            articles_data.append(self._format_article_response(article, article_author, tag_list)["article"])

        return {"articles": articles_data, "articlesCount": len(articles_data)}

    def favorite_article(self, slug: str, user: User) -> dict:
        """Favorite an article"""
        article = self.repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        self.favorite_repo.create(user_id=user.id, article_id=article.id)

        author = self.user_repo.get_by_id(article.author_id)
        tag_list = self.tag_repo.get_tags_for_article(article.id)

        return self._format_article_response(article, author, tag_list, current_user=user)

    def unfavorite_article(self, slug: str, user: User) -> dict:
        """Unfavorite an article"""
        article = self.repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        self.favorite_repo.delete(user_id=user.id, article_id=article.id)

        author = self.user_repo.get_by_id(article.author_id)
        tag_list = self.tag_repo.get_tags_for_article(article.id)

        return self._format_article_response(article, author, tag_list, current_user=user)

    def update_article(
        self, slug: str, user: User, title: str = None, description: str = None, body: str = None
    ) -> dict:
        """Update an article"""
        article = self.repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        # Check if user is the author
        if article.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this article")

        # Update article
        article = self.repo.update(article, title=title, description=description, body=body)

        author = self.user_repo.get_by_id(article.author_id)
        tag_list = self.tag_repo.get_tags_for_article(article.id)

        return self._format_article_response(article, author, tag_list)

    def delete_article(self, slug: str, user: User) -> None:
        """Delete an article"""
        article = self.repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        # Check if user is the author
        if article.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this article")

        self.repo.delete(article)

    def _format_article_response(
        self, article: Article, author: User, tag_list: list[str] = None, current_user: User = None
    ) -> dict:
        """Format article response"""
        favorites_count = self.favorite_repo.count_by_article(article.id)
        favorited = False
        if current_user:
            favorited = self.favorite_repo.is_favorited(current_user.id, article.id)

        return {
            "article": {
                "slug": article.slug,
                "title": article.title,
                "description": article.description,
                "body": article.body,
                "tagList": tag_list or [],
                "createdAt": article.created_at.isoformat() + "Z",
                "updatedAt": article.updated_at.isoformat() + "Z",
                "favoritesCount": favorites_count,
                "favorited": favorited,
                "author": {
                    "username": author.username,
                    "bio": author.bio,
                    "image": author.image,
                    "following": False,
                },
            }
        }
