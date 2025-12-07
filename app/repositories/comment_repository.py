"""Comment Repository"""

from typing import Optional

from sqlmodel import Session, select

from app.models.comment_model import Comment


class CommentRepository:
    """Repository for Comment operations"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, body: str, author_id: int, article_id: int) -> Comment:
        """Create a comment"""
        comment = Comment(body=body, author_id=author_id, article_id=article_id)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by ID"""
        statement = select(Comment).where(Comment.id == comment_id)
        return self.session.exec(statement).first()

    def get_by_article_id(self, article_id: int) -> list[Comment]:
        """Get all comments for an article"""
        statement = select(Comment).where(Comment.article_id == article_id)
        return list(self.session.exec(statement).all())

    def delete(self, comment: Comment) -> None:
        """Delete a comment"""
        self.session.delete(comment)
        self.session.commit()

