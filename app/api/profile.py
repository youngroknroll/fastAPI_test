"""Profile API endpoints"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.services.profile_service import ProfileService

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{username}", status_code=200)
def get_profile(username: str, session: Session = Depends(get_session)):
    """Get user profile by username"""
    service = ProfileService(session)
    return service.get_profile(username)


@router.post("/profiles/{username}/follow", status_code=200)
def follow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Follow a user"""
    service = ProfileService(session)
    return service.follow_user(current_user, username)


@router.delete("/profiles/{username}/follow", status_code=200)
def unfollow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Unfollow a user"""
    service = ProfileService(session)
    return service.unfollow_user(current_user, username)

