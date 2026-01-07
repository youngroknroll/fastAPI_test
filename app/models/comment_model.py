from sqlmodel import Field, SQLModel

from app.models.base import TimestampModel


class Comment(TimestampModel, table=True):
    __tablename__ = "comments"

    id: int | None = Field(default=None, primary_key=True)
    body: str
    author_id: int = Field(foreign_key="users.id")
    article_id: int = Field(foreign_key="articles.id")

