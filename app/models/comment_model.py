"""Comment Model"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Comment(SQLModel, table=True):
    """Comment database model"""

    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str
    author_id: int = Field(foreign_key="users.id")
    article_id: int = Field(foreign_key="articles.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

