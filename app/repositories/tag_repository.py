"""Tag Repository"""

from sqlmodel import Session, select

from app.models.tag_model import ArticleTag, Tag


class TagRepository:
    """Repository for Tag operations"""

    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, name: str) -> Tag:
        """Get existing tag or create new one"""
        statement = select(Tag).where(Tag.name == name)
        tag = self.session.exec(statement).first()
        if not tag:
            tag = Tag(name=name)
            self.session.add(tag)
            self.session.commit()
            self.session.refresh(tag)
        return tag

    def add_tags_to_article(self, article_id: int, tag_names: list[str]) -> None:
        """Add tags to an article"""
        for name in tag_names:
            tag = self.get_or_create(name)
            article_tag = ArticleTag(article_id=article_id, tag_id=tag.id)
            self.session.add(article_tag)
        self.session.commit()

    def get_tags_for_article(self, article_id: int) -> list[str]:
        """Get all tag names for an article"""
        statement = (
            select(Tag.name)
            .join(ArticleTag, Tag.id == ArticleTag.tag_id)
            .where(ArticleTag.article_id == article_id)
        )
        return list(self.session.exec(statement).all())

    def get_article_ids_by_tag(self, tag_name: str) -> list[int]:
        """Get article IDs that have a specific tag"""
        statement = (
            select(ArticleTag.article_id)
            .join(Tag, ArticleTag.tag_id == Tag.id)
            .where(Tag.name == tag_name)
        )
        return list(self.session.exec(statement).all())

    def get_all_tags(self) -> list[str]:
        """Get all tag names"""
        statement = select(Tag.name)
        return list(self.session.exec(statement).all())

