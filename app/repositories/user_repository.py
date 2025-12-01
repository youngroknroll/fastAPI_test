"""User Repository"""

from typing import Optional

from sqlmodel import Session, select

from app.models.user_model import User


class UserRepository:
    """User data access layer"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def create(self, email: str, username: str, password: str) -> User:
        """Create a new user"""
        user = User(email=email, username=username, hashed_password=password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_first_user(self) -> Optional[User]:
        """Get first user (temporary for testing)"""
        statement = select(User)
        return self.session.exec(statement).first()

