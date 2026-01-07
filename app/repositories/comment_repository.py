from sqlmodel import Session, select

from app.models.comment_model import Comment


class CommentRepository:
    """댓글 데이터 저장소"""

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, comment_id: int) -> Comment | None:
        statement = select(Comment).where(Comment.id == comment_id)
        return self._session.exec(statement).first()

    def get_by_article_id(self, article_id: int) -> list[Comment]:
        statement = select(Comment).where(Comment.article_id == article_id)
        return list(self._session.exec(statement).all())

    def create(self, body: str, author_id: int, article_id: int) -> Comment:
        comment = Comment(body=body, author_id=author_id, article_id=article_id)
        self._session.add(comment)
        self._session.commit()
        self._session.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        self._session.delete(comment)
        self._session.commit()
