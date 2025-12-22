"""Comment Service - 댓글 비즈니스 로직"""

from fastapi import HTTPException

from app.models.comment_model import Comment
from app.models.user_model import User
from app.repositories.interfaces import (
    ArticleRepositoryInterface,
    CommentRepositoryInterface,
    UserRepositoryInterface,
)


class CommentService:
    """댓글 관련 비즈니스 로직 처리"""

    def __init__(
        self,
        comment_repo: CommentRepositoryInterface,
        article_repo: ArticleRepositoryInterface,
        user_repo: UserRepositoryInterface,
    ):
        self._comment_repo = comment_repo
        self._article_repo = article_repo
        self._user_repo = user_repo

    def create_comment(self, slug: str, body: str, user: User) -> dict:
        """댓글 작성"""
        article = self._get_article_or_404(slug)
        comment = self._comment_repo.create(body=body, author_id=user.id, article_id=article.id)
        return self._build_comment_response(comment, user)

    def get_comments(self, slug: str) -> dict:
        """게시글의 댓글 목록 조회"""
        article = self._get_article_or_404(slug)
        comments = self._comment_repo.get_by_article_id(article.id)

        comments_data = [
            self._build_comment_response(comment, self._user_repo.get_by_id(comment.author_id))["comment"]
            for comment in comments
        ]
        return {"comments": comments_data}

    def delete_comment(self, slug: str, comment_id: int, user: User) -> None:
        """댓글 삭제"""
        self._get_article_or_404(slug)

        comment = self._comment_repo.get_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        if comment.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this comment")

        self._comment_repo.delete(comment)

    def _get_article_or_404(self, slug: str):
        article = self._article_repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

    def _build_comment_response(self, comment: Comment, author: User) -> dict:
        return {
            "comment": {
                "id": comment.id,
                "body": comment.body,
                "createdAt": comment.created_at.isoformat() + "Z",
                "updatedAt": comment.updated_at.isoformat() + "Z",
                "author": {
                    "username": author.username,
                    "bio": author.bio,
                    "image": author.image,
                    "following": False,
                },
            }
        }
