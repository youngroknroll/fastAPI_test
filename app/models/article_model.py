from datetime import datetime

from sqlmodel import Field, SQLModel


class Article(SQLModel, table=True):

    __tablename__ = "articles"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    title: str
    description: str
    body: str
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

