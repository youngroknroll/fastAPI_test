"""FastAPI dependencies"""

from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import verify_token
from app.models.user_model import User
from app.repositories.user_repository import UserRepository


def get_current_user(
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session),
) -> User:
    """
    Get current user from JWT token

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Extract token from "Token <jwt>"
    try:
        token = authorization.replace("Token ", "")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    # Verify token
    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    # Get user from database
    repo = UserRepository(session)
    user = repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session),
) -> Optional[User]:
    """
    Get current user from JWT token (optional, for public endpoints)

    Returns None if no token provided
    """
    if authorization is None:
        return None

    try:
        return get_current_user(authorization, session)
    except HTTPException:
        return None

