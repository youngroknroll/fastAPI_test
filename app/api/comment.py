"""Comment API - 댓글 관련 엔드포인트"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import get_comment_service, get_current_user
from app.models.user_model import User
from app.services.comment_service import CommentService

router = APIRouter(tags=["comments"])


class CommentCreate(BaseModel):
    body: str


class CommentCreateRequest(BaseModel):
    comment: CommentCreate


@router.post("/articles/{slug}/comments", status_code=200)
def create_comment(
    slug: str,
    request: CommentCreateRequest,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
):
    return service.create_comment(slug=slug, body=request.comment.body, user=current_user)


@router.get("/articles/{slug}/comments", status_code=200)
def get_comments(slug: str, service: CommentService = Depends(get_comment_service)):
    return service.get_comments(slug=slug)


@router.delete("/articles/{slug}/comments/{comment_id}", status_code=204)
def delete_comment(
    slug: str,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
):
    service.delete_comment(slug=slug, comment_id=comment_id, user=current_user)
