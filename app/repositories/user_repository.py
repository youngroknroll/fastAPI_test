"""User Repository - 유저 데이터 접근 계층"""

from typing import Optional

from sqlmodel import Session, select

from app.models.user_model import User


class UserRepository:
    """유저 데이터 저장소"""

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self._session.exec(statement).first()

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self._session.exec(statement).first()

    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self._session.exec(statement).first()

    def create(self, email: str, username: str, password: str) -> User:
        user = User(email=email, username=username, hashed_password=password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user
