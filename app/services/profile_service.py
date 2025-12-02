"""Profile Service - Business logic for profile operations"""

from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.models.user_model import User
from app.repositories.follow_repository import FollowRepository
from app.repositories.user_repository import UserRepository


class ProfileService:
    """Profile business logic"""

    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.follow_repo = FollowRepository(session)

    def get_profile(self, username: str, current_user_id: Optional[int] = None) -> dict:
        """
        Get user profile by username

        Args:
            username: Username to look up
            current_user_id: Current user ID (optional, for checking follow status)

        Returns:
            dict: Profile data with following status

        Raises:
            HTTPException: 404 if profile not found
        """
        user = self.user_repo.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Check if current user is following this profile
        following = False
        if current_user_id is not None:
            following = self.follow_repo.is_following(current_user_id, user.id)

        return {
            "profile": {
                "username": user.username,
                "bio": user.bio,
                "image": user.image,
                "following": following,
            }
        }

    def follow_user(self, current_user: User, username: str) -> dict:
        """
        Follow a user

        Args:
            current_user: Current authenticated user
            username: Username to follow

        Returns:
            dict: Profile data with following=True

        Raises:
            HTTPException: 404 if profile not found, 422 if trying to follow self
        """
        # Get followee
        followee = self.user_repo.get_by_username(username)
        if followee is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Check if trying to follow self
        if current_user.id == followee.id:
            raise HTTPException(status_code=422, detail="Cannot follow yourself")

        # Create follow relationship (if not already following)
        if not self.follow_repo.is_following(current_user.id, followee.id):
            self.follow_repo.create(current_user.id, followee.id)

        return {
            "profile": {
                "username": followee.username,
                "bio": followee.bio,
                "image": followee.image,
                "following": True,
            }
        }

    def unfollow_user(self, current_user: User, username: str) -> dict:
        """
        Unfollow a user

        Args:
            current_user: Current authenticated user
            username: Username to unfollow

        Returns:
            dict: Profile data with following=False

        Raises:
            HTTPException: 404 if profile not found
        """
        # Get followee
        followee = self.user_repo.get_by_username(username)
        if followee is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Delete follow relationship
        self.follow_repo.delete(current_user.id, followee.id)

        return {
            "profile": {
                "username": followee.username,
                "bio": followee.bio,
                "image": followee.image,
                "following": False,
            }
        }

