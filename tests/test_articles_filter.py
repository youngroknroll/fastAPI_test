"""Articles: Filter Tests"""
from tests.conftest import ARTICLE_PAYLOAD, Status


def test_작성자로_검색하면_해당_작성자의_글만_보인다(로그인_유저1_api, 로그인_유저2_api):
    # 유저1이 글 작성
    로그인_유저1_api.create(ARTICLE_PAYLOAD)

    # 유저2가 글 작성
    유저2_payload = {
        "article": {"title": "User2 Article", "description": "Desc2", "body": "Body2"}
    }
    로그인_유저2_api.create(유저2_payload)

    # 작성자 user1로 검색
    조회_결과 = 로그인_유저1_api.list(author="user1")

    assert Status.of(조회_결과) == Status.SUCCESS
    data = 조회_결과.json()
    assert data["articles"][0]["author"]["username"] == "user1"
    assert data["articlesCount"] == 1


def test_태그로_검색하면_해당_태그가_있는_글만_보인다(로그인_유저1_api):
    # python 태그가 있는 글
    python_payload = {
        "article": {
            "title": "Python Article",
            "description": "Desc1",
            "body": "Body1",
            "tagList": ["python", "programming"],
        }
    }
    로그인_유저1_api.create(python_payload)

    # javascript 태그가 있는 글
    js_payload = {
        "article": {
            "title": "JavaScript Article",
            "description": "Desc2",
            "body": "Body2",
            "tagList": ["javascript", "programming"],
        }
    }
    로그인_유저1_api.create(js_payload)

    # python 태그로 검색
    조회_결과 = 로그인_유저1_api.list(tag="python")

    assert Status.of(조회_결과) == Status.SUCCESS
    data = 조회_결과.json()
    assert "python" in data["articles"][0]["tagList"]
    assert data["articlesCount"] == 1


def test_특정_유저가_좋아요한_글만_검색할_수_있다(로그인_유저1_api, 로그인_유저2_api):
    # 유저1이 글 2개 작성
    글1 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    글1_slug = 글1["slug"]

    글2_payload = {
        "article": {"title": "Article Two", "description": "Desc2", "body": "Body2"}
    }
    로그인_유저1_api.create(글2_payload)

    # 유저2가 글1에 좋아요
    로그인_유저2_api.favorite(글1_slug)

    # 유저2가 좋아요한 글 검색
    조회_결과 = 로그인_유저1_api.list(favorited="user2")

    assert Status.of(조회_결과) == Status.SUCCESS
    data = 조회_결과.json()
    assert data["articles"][0]["slug"] == 글1_slug
    assert data["articlesCount"] == 1
