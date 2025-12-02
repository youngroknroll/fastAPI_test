"""Follow Repository"""

from typing import Optional

from sqlmodel import Session, select

from app.models.follow_model import Follow


class FollowRepository:
    """Follow data access layer"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, follower_id: int, followee_id: int) -> Follow:
        """Create a follow relationship"""
        follow = Follow(follower_id=follower_id, followee_id=followee_id)
        self.session.add(follow)
        self.session.commit()
        self.session.refresh(follow)
        return follow

    def delete(self, follower_id: int, followee_id: int) -> bool:
        """Delete a follow relationship"""
        statement = select(Follow).where(
            Follow.follower_id == follower_id, Follow.followee_id == followee_id
        )
        follow = self.session.exec(statement).first()
        if follow:
            self.session.delete(follow)
            self.session.commit()
            return True
        return False

    def is_following(self, follower_id: int, followee_id: int) -> bool:
        """Check if follower is following followee"""
        statement = select(Follow).where(
            Follow.follower_id == follower_id, Follow.followee_id == followee_id
        )
        follow = self.session.exec(statement).first()
        return follow is not None

    def get_by_follower_and_followee(
        self, follower_id: int, followee_id: int
    ) -> Optional[Follow]:
        """Get follow relationship"""
        statement = select(Follow).where(
            Follow.follower_id == follower_id, Follow.followee_id == followee_id
        )
        return self.session.exec(statement).first()

