from sqlmodel import Field, Session, SQLModel, select


class Article(SQLModel, table=True):
    __tablename__ = "articles"
    id: int = Field(primary_key=True)
    title: str
    author: str


class ArticleRepo:
    # 순수 데이터만 접근하도록

    def __init__(self, session: Session):
        self.session = session

    def list(self):
        statement = select(Article)
        return self.session.exec(statement).all()

    def get(self, article_id: int):
        return self.session.get(Article, article_id)

    def create(self, article: Article):
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def update(self, article: Article):
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def delete(self, article: Article):
        self.session.delete(article)
        self.session.commit()
