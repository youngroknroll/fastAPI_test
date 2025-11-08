from app.repositories.article_repo import ArticleRepo


def test_article_create(session):
    """게시글 생성 테스트"""
    # given
    repo = ArticleRepo(session)

    # when: 새로운 글 작성
    created = repo.create(title="test", author="yeong")

    # then: title과 author가 저장되어야 함
    assert created.id is not None
    assert created.title == "test"
    assert created.author == "yeong"

    # when: ID 조회
    found = repo.get(created.id)
    assert found is not None
    assert found.title == "test"


def test_article_list(session):
    """게시글 목록 조회 테스트"""
    # given
    repo = ArticleRepo(session)
    repo.create(title="first", author="yeong")
    repo.create(title="second", author="song")

    # when: 전체 조회
    articles = repo.list()

    # then: 2개 반환
    assert len(articles) == 2


def test_article_update(session):
    """게시글 수정 테스트"""
    # given
    repo = ArticleRepo(session)
    created = repo.create(title="old", author="yeong")

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
    created = repo.create(title="delete", author="yeong")

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
