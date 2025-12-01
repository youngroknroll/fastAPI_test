"""Profile API endpoints"""

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.follow_model import Follow
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
    authorization: str = Header(None),
    session: Session = Depends(get_session),
):
    """Follow a user"""
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Get follower (current user)
    repo = UserRepository(session)
    follower = repo.get_first_user()

    # Get followee
    followee = repo.get_by_username(username)
    if followee is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if trying to follow self
    if follower.id == followee.id:
        raise HTTPException(status_code=422, detail="Cannot follow yourself")

    # Create follow relationship
    follow = Follow(follower_id=follower.id, followee_id=followee.id)
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
    authorization: str = Header(None),
    session: Session = Depends(get_session),
):
    """Unfollow a user"""
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Get follower (current user)
    repo = UserRepository(session)
    follower = repo.get_first_user()

    # Get followee
    followee = repo.get_by_username(username)
    if followee is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Delete follow relationship
    statement = select(Follow).where(
        Follow.follower_id == follower.id, Follow.followee_id == followee.id
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

