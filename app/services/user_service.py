"""User Service - Business logic for user operations"""

from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.core.security import create_access_token
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRegister, UserUpdate


class UserService:
    """User business logic"""

    def __init__(self, session: Session):
        self.session = session
        self.repo = UserRepository(session)

    def register_user(self, user_data: UserRegister) -> dict:
        """
        Register a new user

        Returns:
            dict: User data with token

        Raises:
            HTTPException: 422 if email already exists
        """
        # Check if email already exists
        existing_user = self.repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=422, detail="Email already registered")

        # Create user
        user = self.repo.create(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
        )

        # Generate JWT token
        token = create_access_token(user_id=user.id, username=user.username)

        return {
            "user": {
                "email": user.email,
                "username": user.username,
                "token": token,
            }
        }

    def login_user(self, email: str, password: str) -> dict:
        """
        Login user

        Returns:
            dict: User data with token

        Raises:
            HTTPException: 422 if credentials are invalid
        """
        # Get user by email
        user = self.repo.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=422, detail="Email not found")

        # Check password
        if user.hashed_password != password:
            raise HTTPException(status_code=422, detail="Invalid password")

        # Generate JWT token
        token = create_access_token(user_id=user.id, username=user.username)

        return {
            "user": {
                "email": user.email,
                "username": user.username,
                "token": token,
            }
        }

    def get_user_profile(self, user: User) -> dict:
        """
        Get user profile with token

        Returns:
            dict: User data with token
        """
        token = create_access_token(user_id=user.id, username=user.username)

        return {
            "user": {
                "email": user.email,
                "username": user.username,
                "token": token,
            }
        }

    def update_user(self, user: User, update_data: UserUpdate) -> dict:
        """
        Update user information

        Returns:
            dict: Updated user data with token
        """
        # Update user fields
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.username is not None:
            user.username = update_data.username
        if update_data.password is not None:
            user.hashed_password = update_data.password
        if update_data.bio is not None:
            user.bio = update_data.bio
        if update_data.image is not None:
            user.image = update_data.image

        # Save changes
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        # Generate new token
        token = create_access_token(user_id=user.id, username=user.username)

        return {
            "user": {
                "email": user.email,
                "username": user.username,
                "token": token,
            }
        }

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.repo.get_by_id(user_id)

