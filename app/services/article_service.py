import re

from app.core.error_handlers import get_article_or_404, check_author_permission
from app.models.article_model import Article
from app.models.user_model import User
from app.repositories.interfaces import (
    ArticleRepositoryInterface,
    FavoriteRepositoryInterface,
    TagRepositoryInterface,
    UserRepositoryInterface,
)
from app.dtos.response import ArticleResponse, AuthorResponse


def _slugify(title: str) -> str:
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
    ) -> ArticleResponse:
        slug = _slugify(title)
        article = self._article_repo.create(
            slug=slug, title=title, description=description, body=body, author_id=author.id
        )

        if tag_list:
            self._tag_repo.add_tags_to_article(article.id, tag_list)

        article_data = {
            'article': article,
            'author': author,
            'tag_list': tag_list or [],
            'favorites_count': 0,
            'favorited': False,
        }
        return ArticleResponse.from_article_data(article_data)

    def get_article_by_slug(self, slug: str, current_user_id: int | None = None) -> ArticleResponse:
        article = get_article_or_404(self._article_repo, slug)
        article_data_list = self._article_repo.get_all_with_relations(
            article_ids=[article.id], current_user_id=current_user_id
        )
        if not article_data_list:
            return None
        return ArticleResponse.from_article_data(article_data_list[0])

    def get_articles(self, author: str = None, tag: str = None, favorited: str = None, current_user_id: int | None = None) -> dict:
        author_id = self._get_author_id(author)
        if author and author_id is None:
            return {"articles": [], "articlesCount": 0}

        article_ids = self._get_filtered_article_ids(tag, favorited)
        if article_ids is not None and not article_ids:
            return {"articles": [], "articlesCount": 0}

        articles_data = self._article_repo.get_all_with_relations(
            author_id=author_id, article_ids=article_ids, current_user_id=current_user_id
        )
        articles_response = [
            ArticleResponse.from_article_data(article_data)
            for article_data in articles_data
        ]
        return {"articles": articles_response, "articlesCount": len(articles_response)}

    def update_article(
        self, slug: str, user: User, title: str = None, description: str = None, body: str = None
    ) -> ArticleResponse:
        article = get_article_or_404(self._article_repo, slug)
        check_author_permission(article, user)

        article = self._article_repo.update(article, title=title, description=description, body=body)
        article_data_list = self._article_repo.get_all_with_relations(
            article_ids=[article.id]
        )
        if not article_data_list:
            return None
        return ArticleResponse.from_article_data(article_data_list[0])

    def delete_article(self, slug: str, user: User) -> None:
        article = get_article_or_404(self._article_repo, slug)
        check_author_permission(article, user)
        self._article_repo.delete(article)

    def favorite_article(self, slug: str, user: User) -> ArticleResponse:
        article = get_article_or_404(self._article_repo, slug)

        # 이미 즐겨찾기한 경우 중복 등록 방지
        if not self._favorite_repo.is_favorited(user_id=user.id, article_id=article.id):
            self._favorite_repo.create(user_id=user.id, article_id=article.id)

        article_data_list = self._article_repo.get_all_with_relations(
            article_ids=[article.id], current_user_id=user.id
        )
        if not article_data_list:
            return None
        return ArticleResponse.from_article_data(article_data_list[0])

    def unfavorite_article(self, slug: str, user: User) -> ArticleResponse:
        article = get_article_or_404(self._article_repo, slug)
        self._favorite_repo.delete(user_id=user.id, article_id=article.id)

        article_data_list = self._article_repo.get_all_with_relations(
            article_ids=[article.id], current_user_id=user.id
        )
        if not article_data_list:
            return None
        return ArticleResponse.from_article_data(article_data_list[0])

    # Private methods
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
