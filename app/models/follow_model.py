from sqlmodel import Field, SQLModel


class Follow(SQLModel, table=True):
    __tablename__ = "follows"

    id: int | None = Field(default=None, primary_key=True)
    follower_id: int = Field(foreign_key="users.id")
    followee_id: int = Field(foreign_key="users.id")
