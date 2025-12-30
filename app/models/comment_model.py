from datetime import datetime

from sqlmodel import Field, SQLModel


class Comment(SQLModel, table=True):

    __tablename__ = "comments"

    id: int | None = Field(default=None, primary_key=True)
    body: str
    author_id: int = Field(foreign_key="users.id")
    article_id: int = Field(foreign_key="articles.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

