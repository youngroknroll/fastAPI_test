"""Comment Service - Business logic for comment operations"""

from fastapi import HTTPException
from sqlmodel import Session

from app.models.comment_model import Comment
from app.models.user_model import User
from app.repositories.article_repository import ArticleRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.user_repository import UserRepository


class CommentService:
    """Comment business logic"""

    def __init__(self, session: Session):
        self.session = session
        self.repo = CommentRepository(session)
        self.article_repo = ArticleRepository(session)
        self.user_repo = UserRepository(session)

    def create_comment(self, slug: str, body: str, user: User) -> dict:
        """Create a comment on an article"""
        article = self.article_repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        comment = self.repo.create(body=body, author_id=user.id, article_id=article.id)

        return self._format_comment_response(comment, user)

    def get_comments(self, slug: str) -> dict:
        """Get all comments for an article"""
        article = self.article_repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        comments = self.repo.get_by_article_id(article.id)

        comments_data = []
        for comment in comments:
            author = self.user_repo.get_by_id(comment.author_id)
            comments_data.append(self._format_comment_response(comment, author)["comment"])

        return {"comments": comments_data}

    def delete_comment(self, slug: str, comment_id: int, user: User) -> None:
        """Delete a comment"""
        article = self.article_repo.get_by_slug(slug)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        comment = self.repo.get_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        # Check if user is the author of the comment
        if comment.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this comment")

        self.repo.delete(comment)

    def _format_comment_response(self, comment: Comment, author: User) -> dict:
        """Format comment response"""
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

