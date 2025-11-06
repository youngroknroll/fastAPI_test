from sqlmodel import Field, Session, SQLModel, select


class Article(SQLModel, table=True):
    __tablename__ = "articles"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str

class ArticleRepo:
    def __init__(self, session: Session):
        self.session = session

    def list(self):
        statement = select(Article)
        return self.session.exec(statement).all()

    def get(self, article_id: int) -> Article | None:
        return self.session.get(Article, article_id)

    def create(self, title: str, author: str) -> Article:
        article = Article(title=title, author=author)
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def update(self, article_id: int, title: str, author: str) -> Article:
        article = self.get(article_id)
        if not article:
            return {"error": "article not found"}
        article.title = title
        article.author = author

        try:
            self.session.add(article)
            self.session.commit()
            self.session.refresh(article)
        except Exception:
            self.session.rollback()
            raise
        return article
