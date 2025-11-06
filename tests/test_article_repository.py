from pickletools import read_stringnl_noescape_pair

from app.repositories.article_repo import ArticleRepo


def test_article_create(session):
    #given
    repo = ArticleRepo(session)

    #when 새로운 글 작성
    created = repo.create(title="test", author="yeong")

    #then title과 author가 저장되어야함
    assert created.id == 1
    assert created.title == "test"

    # # when 전체 조회
    # articles = repo.list()
    # assert len(articles) == 1

    # when ID 조회
    found = repo.get(created.id)
    assert found.title == "test"

def test_article_update(session):
    #given
    repo = ArticleRepo(session)
    created = repo.create(title="old", author="yeong")

    #when
    updated = repo.update(article_id=created.id, title="new", author="song")

    #then
    assert updated is not None
    assert updated.title == "new"
    assert updated.author == "song"

def test_article_delete(session):
    #given
    repo = ArticleRepo(session)
    created = repo.create(title="delete", author="yeong")

    #when
    result = repo.delete(created.id)

    #then
    assert result is True
    assert repo.get(created.id) is None




