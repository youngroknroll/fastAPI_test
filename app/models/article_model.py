"""Article Model"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Article(SQLModel, table=True):
    """Article database model"""

    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    title: str
    description: str
    body: str
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

