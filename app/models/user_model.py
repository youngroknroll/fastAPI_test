from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    bio: Optional[str] = None
    image: Optional[str] = None

