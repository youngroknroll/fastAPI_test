from typing import Any

from sqlmodel import Session, select, func

from app.models.article_model import Article
from app.models.favorite_model import Favorite
from app.models.tag_model import Tag, ArticleTag
from app.models.user_model import User


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
        self, author_id: int | None = None, article_ids: list[int] | None = None,
        current_user_id: int | None = None
    ) -> list[dict]:
        """모든 관계 데이터를 포함하여 게시글 조회 (배치)"""
        # 기본 게시글 조회
        statement = select(Article)
        if author_id is not None:
            statement = statement.where(Article.author_id == author_id)
        if article_ids is not None:
            statement = statement.where(Article.id.in_(article_ids))
        
        articles = list(self._session.exec(statement).all())
        
        if not articles:
            return []
        
        article_ids_set = {a.id for a in articles}
        
        # 모든 작성자 데이터 배치 조회
        author_ids = {a.author_id for a in articles}
        author_statement = select(User).where(User.id.in_(author_ids))
        authors = {u.id: u for u in self._session.exec(author_statement).all()}
        
        # 모든 태그 데이터 배치 조회
        tag_statement = (
            select(ArticleTag.article_id, Tag.name)
            .join(Tag, ArticleTag.tag_id == Tag.id)
            .where(ArticleTag.article_id.in_(article_ids_set))
        )
        article_tags = {}
        for article_id, tag_name in self._session.exec(tag_statement).all():
            if article_id not in article_tags:
                article_tags[article_id] = []
            article_tags[article_id].append(tag_name)
        
        # 즐겨찾기 카운트 배치 조회
        favorite_count_statement = (
            select(Favorite.article_id, func.count(Favorite.article_id).label('count'))
            .where(Favorite.article_id.in_(article_ids_set))
            .group_by(Favorite.article_id)
        )
        favorite_counts = {}
        for article_id, count in self._session.exec(favorite_count_statement).all():
            favorite_counts[article_id] = count
        
        # 현재 사용자의 즐겨찾기 여부 배치 조회
        favorited_map = {}
        if current_user_id:
            favorited_statement = (
                select(Favorite.article_id)
                .where(Favorite.user_id == current_user_id)
                .where(Favorite.article_id.in_(article_ids_set))
            )
            favorited_article_ids = set(self._session.exec(favorited_statement).all())
            for article_id in article_ids_set:
                favorited_map[article_id] = article_id in favorited_article_ids
        else:
            for article_id in article_ids_set:
                favorited_map[article_id] = False
        
        # 응답 데이터 조립
        result = []
        for article in articles:
            result.append({
                'article': article,
                'author': authors.get(article.author_id),
                'tag_list': article_tags.get(article.id, []),
                'favorites_count': favorite_counts.get(article.id, 0),
                'favorited': favorited_map.get(article.id, False),
            })
        
        return result
