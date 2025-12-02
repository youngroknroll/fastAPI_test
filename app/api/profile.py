"""Profile API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.follow_model import Follow
from app.models.user_model import User
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{username}", status_code=200)
def get_profile(username: str, session: Session = Depends(get_session)):
    """Get user profile by username"""
    repo = UserRepository(session)
    user = repo.get_by_username(username)

    if user is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "profile": {
            "username": user.username,
            "bio": user.bio,
            "image": user.image,
            "following": False,
        }
    }


@router.post("/profiles/{username}/follow", status_code=200)
def follow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Follow a user"""
    # Get followee
    repo = UserRepository(session)
    followee = repo.get_by_username(username)
    if followee is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if trying to follow self
    if current_user.id == followee.id:
        raise HTTPException(status_code=422, detail="Cannot follow yourself")

    # Create follow relationship
    follow = Follow(follower_id=current_user.id, followee_id=followee.id)
    session.add(follow)
    session.commit()

    return {
        "profile": {
            "username": followee.username,
            "bio": followee.bio,
            "image": followee.image,
            "following": True,
        }
    }


@router.delete("/profiles/{username}/follow", status_code=200)
def unfollow_user(
    username: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Unfollow a user"""
    # Get followee
    repo = UserRepository(session)
    followee = repo.get_by_username(username)
    if followee is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Delete follow relationship
    statement = select(Follow).where(
        Follow.follower_id == current_user.id, Follow.followee_id == followee.id
    )
    follow = session.exec(statement).first()
    if follow:
        session.delete(follow)
        session.commit()

    return {
        "profile": {
            "username": followee.username,
            "bio": followee.bio,
            "image": followee.image,
            "following": False,
        }
    }

