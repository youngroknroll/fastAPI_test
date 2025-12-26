from sqlmodel import Session, select

from app.models.tag_model import ArticleTag, Tag


class TagRepository:

    def __init__(self, session: Session):
        self._session = session

    def add_tags_to_article(self, article_id: int, tag_names: list[str]) -> None:
        for name in tag_names:
            tag = self._get_or_create(name)
            article_tag = ArticleTag(article_id=article_id, tag_id=tag.id)
            self._session.add(article_tag)
        self._session.commit()

    def get_tags_for_article(self, article_id: int) -> list[str]:
        statement = (
            select(Tag.name)
            .join(ArticleTag, Tag.id == ArticleTag.tag_id)
            .where(ArticleTag.article_id == article_id)
        )
        return list(self._session.exec(statement).all())

    def get_article_ids_by_tag(self, tag_name: str) -> list[int]:
        statement = (
            select(ArticleTag.article_id)
            .join(Tag, ArticleTag.tag_id == Tag.id)
            .where(Tag.name == tag_name)
        )
        return list(self._session.exec(statement).all())

    def get_all_tags(self) -> list[str]:
        statement = select(Tag.name)
        return list(self._session.exec(statement).all())

    def _get_or_create(self, name: str) -> Tag:
        statement = select(Tag).where(Tag.name == name)
        tag = self._session.exec(statement).first()
        if not tag:
            tag = Tag(name=name)
            self._session.add(tag)
            self._session.commit()
            self._session.refresh(tag)
        return tag
