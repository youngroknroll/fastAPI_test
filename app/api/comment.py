"""Comment API - 댓글 관련 엔드포인트"""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_comment_service, get_current_user
from app.models.user_model import User
from app.dtos.request import CommentCreateRequest
from app.dtos.response import CommentResponseWrapper, SingleCommentResponseWrapper
from app.services.comment_service import CommentService

router = APIRouter(tags=["comments"])


@router.post("/articles/{slug}/comments", status_code=200, response_model=SingleCommentResponseWrapper)
def create_comment(
    slug: str,
    request: CommentCreateRequest,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
):
    comment_dto = service.create_comment(slug=slug, body=request.comment.body, user=current_user)
    return {"comment": comment_dto}


@router.get("/articles/{slug}/comments", status_code=200, response_model=CommentResponseWrapper)
def get_comments(slug: str, service: CommentService = Depends(get_comment_service)):
    comments = service.get_comments(slug=slug)
    return {"comments": comments}


@router.delete("/articles/{slug}/comments/{comment_id}", status_code=204)
def delete_comment(
    slug: str,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
):
    service.delete_comment(slug=slug, comment_id=comment_id, user=current_user)
