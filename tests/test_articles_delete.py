from tests.conftest import ARTICLE_PAYLOAD, Status


def test_유저는_자신의_게시글을_삭제할_수_있다(로그인_유저1_api):
    created_article = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = created_article["slug"]

    삭제_결과 = 로그인_유저1_api.delete(slug)
    assert Status.of(삭제_결과) == Status.DELETED

    조회_결과 = 로그인_유저1_api.get(slug)
    assert Status.of(조회_결과) == Status.NOT_FOUND


def test_다른_사람의_게시글은_삭제할_수_없다(로그인_유저1_api, 로그인_유저2_api):
    created_article = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = created_article["slug"]

    삭제_결과 = 로그인_유저2_api.delete(slug)
    assert Status.of(삭제_결과) == Status.FORBIDDEN


def test_존재하지_않는_게시글은_삭제할_수_없다(로그인_유저1_api):
    non_exist_slug = "non-existent-slug"

    삭제_결과 = 로그인_유저1_api.delete(non_exist_slug)
    assert Status.of(삭제_결과) == Status.NOT_FOUND


def test_로그인하지_않으면_게시글을_삭제할_수_없다(로그인_유저1_api, 게스트_api):
    created_article = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = created_article["slug"]

    삭제_결과 = 게스트_api.delete(slug)
    assert Status.of(삭제_결과) == Status.UNAUTHORIZED
