from fastapi import HTTPException

from app.core.error_handlers import get_article_or_404, check_comment_author_permission
from app.models.comment_model import Comment
from app.models.user_model import User
from app.repositories.interfaces import (
    ArticleRepositoryInterface,
    CommentRepositoryInterface,
    UserRepositoryInterface,
)
from app.dtos.response import CommentResponse, AuthorResponse


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepositoryInterface,
        article_repo: ArticleRepositoryInterface,
        user_repo: UserRepositoryInterface,
    ):
        self._comment_repo = comment_repo
        self._article_repo = article_repo
        self._user_repo = user_repo

    def create_comment(self, slug: str, body: str, user: User) -> CommentResponse:
        article = get_article_or_404(self._article_repo, slug)
        comment = self._comment_repo.create(body=body, author_id=user.id, article_id=article.id)
        return self._build_comment_response(comment, user)

    def get_comments(self, slug: str) -> list[CommentResponse]:
        article = get_article_or_404(self._article_repo, slug)
        comments = self._comment_repo.get_by_article_id(article.id)

        comments_data = [
            self._build_comment_response(comment, self._user_repo.get_by_id(comment.author_id))
            for comment in comments
        ]
        return comments_data

    def delete_comment(self, slug: str, comment_id: int, user: User) -> None:
        get_article_or_404(self._article_repo, slug)

        comment = self._comment_repo.get_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        check_comment_author_permission(comment.author_id, user.id)
        self._comment_repo.delete(comment)
    def _build_comment_response(self, comment: Comment, author: User) -> CommentResponse:
        return CommentResponse(
            id=comment.id,
            body=comment.body,
            createdAt=comment.created_at.isoformat() + "Z",
            updatedAt=comment.updated_at.isoformat() + "Z",
            author=AuthorResponse.from_user(author),
        )

