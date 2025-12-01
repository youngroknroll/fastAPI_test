"""Profile API endpoints"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{username}", status_code=200)
def get_profile(username: str, session: Session = Depends(get_session)):
    """Get user profile by username"""
    repo = UserRepository(session)
    user = repo.get_by_username(username)

    return {
        "profile": {
            "username": user.username,
            "bio": user.bio,
            "image": user.image,
            "following": False,
        }
    }

