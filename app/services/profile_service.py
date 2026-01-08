from fastapi import HTTPException

from app.models.user_model import User
from app.repositories.interfaces import FollowRepositoryInterface, UserRepositoryInterface
from app.dtos.response import ProfileResponse


class ProfileService:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        follow_repo: FollowRepositoryInterface,
    ):
        self._user_repo = user_repo
        self._follow_repo = follow_repo

    def get_profile(self, username: str, current_user_id: int | None = None) -> ProfileResponse:
        user = self._get_user_or_404(username)
        following = (
            self._follow_repo.is_following(current_user_id, user.id)
            if current_user_id
            else False
        )
        return ProfileResponse.from_user(user, following)

    def follow_user(self, current_user: User, username: str) -> ProfileResponse:
        followee = self._get_user_or_404(username)

        if current_user.id == followee.id:
            raise HTTPException(status_code=422, detail="Cannot follow yourself")

        if not self._follow_repo.is_following(current_user.id, followee.id):
            self._follow_repo.create(current_user.id, followee.id)

        return ProfileResponse.from_user(followee, following=True)

    def unfollow_user(self, current_user: User, username: str) -> ProfileResponse:
        followee = self._get_user_or_404(username)
        self._follow_repo.delete(current_user.id, followee.id)
        return ProfileResponse.from_user(followee, following=False)

    def _get_user_or_404(self, username: str) -> User:
        user = self._user_repo.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        return user

