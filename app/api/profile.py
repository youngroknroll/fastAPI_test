"""Profile API - 프로필 관련 엔드포인트"""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_profile_service
from app.models.user_model import User
from app.dtos.response import ProfileResponseWrapper
from app.services.profile_service import ProfileService

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{username}", status_code=200, response_model=ProfileResponseWrapper)
def get_profile(username: str, service: ProfileService = Depends(get_profile_service)):
    profile = service.get_profile(username)
    return {"profile": profile}


@router.post("/profiles/{username}/follow", status_code=200, response_model=ProfileResponseWrapper)
def follow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    profile = service.follow_user(current_user, username)
    return {"profile": profile}


@router.delete("/profiles/{username}/follow", status_code=200, response_model=ProfileResponseWrapper)
def unfollow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    profile = service.unfollow_user(current_user, username)
    return {"profile": profile}
