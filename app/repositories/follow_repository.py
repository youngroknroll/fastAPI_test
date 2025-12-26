from sqlmodel import Session, select

from app.models.follow_model import Follow


class FollowRepository:

    def __init__(self, session: Session):
        self._session = session

    def create(self, follower_id: int, followee_id: int) -> Follow:
        follow = Follow(follower_id=follower_id, followee_id=followee_id)
        self._session.add(follow)
        self._session.commit()
        self._session.refresh(follow)
        return follow

    def delete(self, follower_id: int, followee_id: int) -> bool:
        statement = select(Follow).where(
            Follow.follower_id == follower_id, Follow.followee_id == followee_id
        )
        follow = self._session.exec(statement).first()
        if follow:
            self._session.delete(follow)
            self._session.commit()
            return True
        return False

    def is_following(self, follower_id: int, followee_id: int) -> bool:
        statement = select(Follow).where(
            Follow.follower_id == follower_id, Follow.followee_id == followee_id
        )
        follow = self._session.exec(statement).first()
        return follow is not None
