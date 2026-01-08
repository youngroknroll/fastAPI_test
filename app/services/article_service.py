import re

from app.core.error_handlers import get_article_or_404, check_author_permission
from app.models.user_model import User
from app.repositories.article_repository import ArticleWithRelations
from app.repositories.interfaces import (
    ArticleRepositoryInterface,
    FavoriteRepositoryInterface,
    TagRepositoryInterface,
    UserRepositoryInterface,
)
from app.dtos.response import ArticleResponse, ArticleResponseWrapper


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
        self,
        title: str,
        description: str,
        body: str,
        author: User,
        tag_list: list[str] | None = None,
    ) -> ArticleResponse:
        slug = self._slugify(title)
        article = self._article_repo.create(
            slug=slug,
            title=title,
            description=description,
            body=body,
            author_id=author.id,
        )

        if tag_list:
            self._tag_repo.add_tags_to_article(article.id, tag_list)

        article_data = ArticleWithRelations(
            article=article,
            author=author,
            tag_list=tag_list or [],
            favorites_count=0,
            favorited=False,
        )
        return ArticleResponse.from_article_data(article_data)

    def get_article_by_slug(
        self, slug: str, current_user_id: int | None = None
    ) -> ArticleResponse | None:
        article = get_article_or_404(self._article_repo, slug)
        return self._get_article_response(article.id, current_user_id)

    def get_articles(
        self,
        author: str | None = None,
        tag: str | None = None,
        favorited: str | None = None,
        current_user_id: int | None = None,
    ) -> ArticleResponseWrapper:
        author_id = self._get_author_id(author)
        if author and author_id is None:
            return ArticleResponseWrapper(articles=[], articlesCount=0)

        article_ids = self._get_filtered_article_ids(tag, favorited)
        if article_ids is not None and not article_ids:
            return ArticleResponseWrapper(articles=[], articlesCount=0)

        articles_data = self._article_repo.get_all_with_relations(
            author_id=author_id,
            article_ids=article_ids,
            current_user_id=current_user_id,
        )
        articles_response = [
            ArticleResponse.from_article_data(article_data)
            for article_data in articles_data
        ]
        return ArticleResponseWrapper(
            articles=articles_response,
            articlesCount=len(articles_response),
        )

    def update_article(
        self,
        slug: str,
        user: User,
        title: str | None = None,
        description: str | None = None,
        body: str | None = None,
    ) -> ArticleResponse | None:
        article = get_article_or_404(self._article_repo, slug)
        check_author_permission(article, user)

        updated_article = self._article_repo.update(
            article, title=title, description=description, body=body
        )
        return self._get_article_response(updated_article.id)

    def delete_article(self, slug: str, user: User) -> None:
        article = get_article_or_404(self._article_repo, slug)
        check_author_permission(article, user)
        self._article_repo.delete(article)

    def favorite_article(self, slug: str, user: User) -> ArticleResponse | None:
        article = get_article_or_404(self._article_repo, slug)

        if not self._favorite_repo.is_favorited(user_id=user.id, article_id=article.id):
            self._favorite_repo.create(user_id=user.id, article_id=article.id)

        return self._get_article_response(article.id, user.id)

    def unfavorite_article(self, slug: str, user: User) -> ArticleResponse | None:
        article = get_article_or_404(self._article_repo, slug)
        self._favorite_repo.delete(user_id=user.id, article_id=article.id)
        return self._get_article_response(article.id, user.id)

    # Private methods
    def _get_article_response(
        self, article_id: int, current_user_id: int | None = None
    ) -> ArticleResponse | None:
        """단일 게시글 응답 생성 (중복 제거용)"""
        article_data_list = self._article_repo.get_all_with_relations(
            article_ids=[article_id], current_user_id=current_user_id
        )
        if not article_data_list:
            return None
        return ArticleResponse.from_article_data(article_data_list[0])

    def _get_author_id(self, username: str | None) -> int | None:
        if not username:
            return None
        user = self._user_repo.get_by_username(username)
        return user.id if user else None

    def _get_filtered_article_ids(
        self, tag: str | None, favorited: str | None
    ) -> list[int] | None:
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
            if article_ids:
                article_ids = list(set(article_ids) & set(favorited_ids))
            else:
                article_ids = favorited_ids

        return article_ids

    @staticmethod
    def _slugify(title: str) -> str:
        slug = title.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        return slug.strip("-")
