"""Comment API Router"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.services.comment_service import CommentService

router = APIRouter(tags=["comments"])


class CommentCreate(BaseModel):
    """Comment create schema"""

    body: str


class CommentCreateRequest(BaseModel):
    """Comment create request wrapper"""

    comment: CommentCreate


@router.post("/articles/{slug}/comments", status_code=200)
def create_comment(
    slug: str,
    request: CommentCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a comment on an article"""
    service = CommentService(session)
    return service.create_comment(slug=slug, body=request.comment.body, user=current_user)


@router.get("/articles/{slug}/comments", status_code=200)
def get_comments(slug: str, session: Session = Depends(get_session)):
    """Get all comments for an article"""
    service = CommentService(session)
    return service.get_comments(slug=slug)


@router.delete("/articles/{slug}/comments/{comment_id}", status_code=204)
def delete_comment(
    slug: str,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a comment"""
    service = CommentService(session)
    service.delete_comment(slug=slug, comment_id=comment_id, user=current_user)

