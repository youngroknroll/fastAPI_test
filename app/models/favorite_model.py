from sqlmodel import Field, SQLModel


class Favorite(SQLModel, table=True):

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    article_id: int = Field(foreign_key="articles.id", primary_key=True)

