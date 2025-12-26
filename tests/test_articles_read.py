from tests.conftest import ARTICLE_PAYLOAD, Status


def test_게시글_목록을_조회할_수_있다(게스트_api):
    조회_결과 = 게스트_api.list()

    assert Status.of(조회_결과) == Status.SUCCESS
    data = 조회_결과.json()
    assert "articlesCount" in data
    assert isinstance(data["articlesCount"], int)


def test_특정_게시글을_조회할_수_있다(로그인_유저1_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]

    조회_결과 = 로그인_유저1_api.get(slug)

    assert Status.of(조회_결과) == Status.SUCCESS
    data = 조회_결과.json()
    assert "article" in data
    assert data["article"]["slug"] == slug


def test_존재하지_않는_게시글은_조회할_수_없다(게스트_api):
    조회_결과 = 게스트_api.get("nonexistent-slug")

    assert Status.of(조회_결과) == Status.NOT_FOUND
