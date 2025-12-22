"""Articles: Update Tests"""
from tests.conftest import ARTICLE_PAYLOAD, Status


def test_자신의_게시글을_수정할_수_있다(로그인_유저1_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]

    새_내용 = {"article": {"title": "Updated Title"}}
    수정_결과 = 로그인_유저1_api.update(slug, 새_내용)

    assert Status.of(수정_결과) == Status.SUCCESS
    assert 수정_결과.json()["article"]["title"] == "Updated Title"


def test_다른_사람의_게시글은_수정할_수_없다(로그인_유저1_api, 로그인_유저2_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]

    새_내용 = {"article": {"title": "Hacked Title"}}
    수정_결과 = 로그인_유저2_api.update(slug, 새_내용)

    assert Status.of(수정_결과) == Status.FORBIDDEN


def test_존재하지_않는_게시글은_수정할_수_없다(로그인_유저1_api):
    존재하지_않는_slug = "non-existent-slug"

    새_내용 = {"article": {"title": "Updated Title"}}
    수정_결과 = 로그인_유저1_api.update(존재하지_않는_slug, 새_내용)

    assert Status.of(수정_결과) == Status.NOT_FOUND
