from app.repositories.article_repo import ArticleRepo
from app.schemas.article_schema import ArticleCreate

    

def test_article_create(session):
    """게시글 생성 테스트"""
    # given
    repo = ArticleRepo(session)
    data = ArticleCreate(title="test", author="yeong", slug="test")

    # when: 새로운 글 작성
    created = repo.create(data)

    # then: title과 author가 저장되어야 함
    assert created.id is not None
    assert created.title == "test"
    assert created.author == "yeong"
    assert created.slug == "test"

    # and : ID로 조회 되어야 함
    found = repo.get(created.id)
    assert found is not None
    assert found.title == "test"


def test_article_list(session):
    """게시글 목록 조회 테스트"""
    # given
    repo = ArticleRepo(session)
    repo.create(ArticleCreate(title="first", author="yeong", slug="first"))
    repo.create(ArticleCreate(title="second", author="song", slug="second"))

    # when: 전체 조회
    articles = repo.list()

    # then: 2개 반환
    assert len(articles) == 2


def test_article_update(session):
    """게시글 수정 테스트"""
    # given
    repo = ArticleRepo(session)
    data = ArticleCreate(title="old", author="yeong", slug="old")
    created = repo.create(data)

    # when: 수정
    updated = repo.update(article_id=created.id, title="new", author="song")

    # then: 수정 확인
    assert updated is not None
    assert updated.title == "new"
    assert updated.author == "song"


def test_article_update_not_found(session):
    """존재하지 않는 게시글 수정 시 None 반환"""
    # given
    repo = ArticleRepo(session)

    # when: 존재하지 않는 ID로 수정
    result = repo.update(article_id=999, title="new", author="song")

    # then: None 반환
    assert result is None


def test_article_delete(session):
    """게시글 삭제 테스트"""
    # given
    repo = ArticleRepo(session)
    data = ArticleCreate(title="delete", author="yeong", slug="delete")
    created = repo.create(data)

    # when: 삭제
    result = repo.delete(created.id)

    # then: 삭제 성공
    assert result is True
    assert repo.get(created.id) is None


def test_article_delete_not_found(session):
    """존재하지 않는 게시글 삭제 시 False 반환"""
    # given
    repo = ArticleRepo(session)

    # when: 존재하지 않는 ID로 삭제
    result = repo.delete(999)

    # then: False 반환
    assert result is False


def test_article_has_slug(session):
    """Article은 slug 필드를 가지고 있어야 한다."""
    # given : "Hello World"라는 제목과 "hello-world"라는 slug가 있는 Article
    repo = ArticleRepo(session)
    data = ArticleCreate(title="Hello World", author="yeong", slug="hello-world")
    # when : 게시글 작성하면
    created = repo.create(data)
    # then : slug 필드가 있는 게시글이 생성되어야 한다
    assert created.slug == "hello-world"
    assert created.id is not None
    
    # and : 조회도 가능해야한다.
    found = repo.get(created.id)
    assert found.slug == "hello-world"
    