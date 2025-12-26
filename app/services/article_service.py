import re

from fastapi import HTTPException

from app.models.article_model import Article
from app.models.user_model import User
from app.repositories.interfaces import (
    ArticleRepositoryInterface,
    FavoriteRepositoryInterface,
    TagRepositoryInterface,
    UserRepositoryInterface,
)


def _slugify(title: str) -> str:
    """제목을 slug로 변환"""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


class ArticleService:

    def __init__(
        self,
        article_repo: ArticleRepositoryInterface,
        user_repo: UserRepositoryInterface,
        tag_repo: TagRepositoryInterface,
        favorite_repo: FavoriteRepositoryInterface,
    ):
        self._article_repo = article_repo
        self._user_repo = user_repo
        self._tag_repo = tag_repo
        self._favorite_repo = favorite_repo

    def create_article(
        self, title: str, description: str, body: str, author: User, tag_list: list[str] = None
    ) -> dict:
        """게시글 작성"""
        slug = _slugify(title)
        article = self._article_repo.create(
            slug=slug, title=title, description=description, body=body, author_id=author.id
        )

        if tag_list:
            self._tag_repo.add_tags_to_article(article.id, tag_list)

        return self._build_article_response(article, author, tag_list or [])

    def get_article_by_slug(self, slug: str) -> dict:
        """slug로 게시글 조회"""
        article = self._get_article_or_404(slug)
        author = self._user_repo.get_by_id(article.author_id)
        tag_list = self._tag_repo.get_tags_for_article(article.id)
        return self._build_article_response(article, author, tag_list)

    def get_articles(self, author: str = None, tag: str = None, favorited: str = None) -> dict:
        """게시글 목록 조회 (필터링 가능)"""
        author_id = self._get_author_id(author)
        if author and author_id is None:
            return {"articles": [], "articlesCount": 0}

        article_ids = self._get_filtered_article_ids(tag, favorited)
        if article_ids is not None and not article_ids:
            return {"articles": [], "articlesCount": 0}

        articles = self._article_repo.get_all(author_id=author_id, article_ids=article_ids)
        articles_data = [
            self._build_article_response(
                article,
                self._user_repo.get_by_id(article.author_id),
                self._tag_repo.get_tags_for_article(article.id),
            )["article"]
            for article in articles
        ]
        return {"articles": articles_data, "articlesCount": len(articles_data)}

    def update_article(
        self, slug: str, user: User, title: str = None, description: str = None, body: str = None
    ) -> dict:
        """게시글 수정"""
        article = self._get_article_or_404(slug)
        self._check_author_permission(article, user)

        article = self._article_repo.update(article, title=title, description=description, body=body)
        author = self._user_repo.get_by_id(article.author_id)
        tag_list = self._tag_repo.get_tags_for_article(article.id)
        return self._build_article_response(article, author, tag_list)

    def delete_article(self, slug: str, user: User) -> None:
        """게시글 삭제"""
        article = self._get_article_or_404(slug)
        self._check_author_permission(article, user)
        self._article_repo.delete(article)

    def favorite_article(self, slug: str, user: User) -> dict:
        """게시글 좋아요"""
        article = self._get_article_or_404(slug)
        self._favorite_repo.create(user_id=user.id, article_id=article.id)

        author = self._user_repo.get_by_id(article.author_id)
        tag_list = self._tag_repo.get_tags_for_article(article.id)
        return self._build_article_response(article, author, tag_list, current_user=user)

    def unfavorite_article(self, slug: str, user: User) -> dict:
        """게시글 좋아요 취소"""
        article = self._get_article_or_404(slug)
        self._favorite_repo.delete(user_id=user.id, article_id=article.id)

        author = self._user_repo.get_by_id(article.author_id)
        tag_list = self._tag_repo.get_tags_for_article(article.id)
        return self._build_article_response(article, author, tag_list, current_user=user)

    # Private methods
    def _get_article_or_404(self, slug: str) -> Article:
        article = self._article_repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

    def _check_author_permission(self, article: Article, user: User) -> None:
        if article.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this article")

    def _get_author_id(self, username: str) -> int | None:
        if not username:
            return None
        user = self._user_repo.get_by_username(username)
        return user.id if user else None

    def _get_filtered_article_ids(self, tag: str, favorited: str) -> list[int] | None:
        article_ids = None

        if tag:
            article_ids = self._tag_repo.get_article_ids_by_tag(tag)
            if not article_ids:
                return []

        if favorited:
            user = self._user_repo.get_by_username(favorited)
            if not user:
                return []
            favorited_ids = self._favorite_repo.get_article_ids_by_user(user.id)
            if not favorited_ids:
                return []
            article_ids = list(set(article_ids) & set(favorited_ids)) if article_ids else favorited_ids

        return article_ids

    def _build_article_response(
        self, article: Article, author: User, tag_list: list[str] = None, current_user: User = None
    ) -> dict:
        favorites_count = self._favorite_repo.count_by_article(article.id)
        favorited = (
            self._favorite_repo.is_favorited(current_user.id, article.id) if current_user else False
        )

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
