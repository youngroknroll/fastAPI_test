from typing import Any, TypedDict

from sqlmodel import Session, select, func

from app.models.article_model import Article
from app.models.favorite_model import Favorite
from app.models.tag_model import Tag, ArticleTag
from app.models.user_model import User


class ArticleWithRelations(TypedDict):
    article: Article
    author: User | None
    tag_list: list[str]
    favorites_count: int
    favorited: bool


class ArticleRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_slug(self, slug: str) -> Article | None:
        statement = select(Article).where(Article.slug == slug)
        return self._session.exec(statement).first()

    def get_all(
        self, author_id: int | None = None, article_ids: list[int] | None = None
    ) -> list[Article]:
        statement = select(Article)
        if author_id is not None:
            statement = statement.where(Article.author_id == author_id)
        if article_ids is not None:
            statement = statement.where(Article.id.in_(article_ids))
        return list(self._session.exec(statement).all())

    def create(
        self, slug: str, title: str, description: str, body: str, author_id: int
    ) -> Article:
        article = Article(
            slug=slug, title=title, description=description, body=body, author_id=author_id
        )
        self._session.add(article)
        self._session.commit()
        self._session.refresh(article)
        return article

    def update(self, article: Article, **kwargs: Any) -> Article:
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

    def get_all_with_relations(
        self,
        author_id: int | None = None,
        article_ids: list[int] | None = None,
        current_user_id: int | None = None,
    ) -> list[ArticleWithRelations]:
        """모든 관계 데이터를 포함하여 게시글 조회 (배치)"""
        articles = self._fetch_articles(author_id, article_ids)
        if not articles:
            return []

        article_id_set = {article.id for article in articles}
        author_id_set = {article.author_id for article in articles}

        authors = self._fetch_authors_batch(author_id_set)
        tags = self._fetch_tags_batch(article_id_set)
        favorite_counts = self._fetch_favorite_counts_batch(article_id_set)
        favorited_map = self._fetch_favorited_batch(article_id_set, current_user_id)

        return [
            ArticleWithRelations(
                article=article,
                author=authors.get(article.author_id),
                tag_list=tags.get(article.id, []),
                favorites_count=favorite_counts.get(article.id, 0),
                favorited=favorited_map.get(article.id, False),
            )
            for article in articles
        ]

    def _fetch_articles(
        self, author_id: int | None, article_ids: list[int] | None
    ) -> list[Article]:
        statement = select(Article)
        if author_id is not None:
            statement = statement.where(Article.author_id == author_id)
        if article_ids is not None:
            statement = statement.where(Article.id.in_(article_ids))
        return list(self._session.exec(statement).all())

    def _fetch_authors_batch(self, author_ids: set[int]) -> dict[int, User]:
        statement = select(User).where(User.id.in_(author_ids))
        return {user.id: user for user in self._session.exec(statement).all()}

    def _fetch_tags_batch(self, article_ids: set[int]) -> dict[int, list[str]]:
        statement = (
            select(ArticleTag.article_id, Tag.name)
            .join(Tag, ArticleTag.tag_id == Tag.id)
            .where(ArticleTag.article_id.in_(article_ids))
        )
        result: dict[int, list[str]] = {}
        for article_id, tag_name in self._session.exec(statement).all():
            result.setdefault(article_id, []).append(tag_name)
        return result

    def _fetch_favorite_counts_batch(self, article_ids: set[int]) -> dict[int, int]:
        statement = (
            select(Favorite.article_id, func.count(Favorite.article_id))
            .where(Favorite.article_id.in_(article_ids))
            .group_by(Favorite.article_id)
        )
        return {
            article_id: count
            for article_id, count in self._session.exec(statement).all()
        }

    def _fetch_favorited_batch(
        self, article_ids: set[int], user_id: int | None
    ) -> dict[int, bool]:
        if not user_id:
            return {article_id: False for article_id in article_ids}

        statement = (
            select(Favorite.article_id)
            .where(Favorite.user_id == user_id)
            .where(Favorite.article_id.in_(article_ids))
        )
        favorited_ids = set(self._session.exec(statement).all())
        return {
            article_id: article_id in favorited_ids
            for article_id in article_ids
        }
