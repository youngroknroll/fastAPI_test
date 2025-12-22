"""Articles: Create Tests"""
from tests.conftest import ARTICLE_PAYLOAD, Status


def test_로그인한_유저는_게시글을_작성할_수_있다(로그인_유저1_api):
    response = 로그인_유저1_api.create(ARTICLE_PAYLOAD)

    assert Status.of(response) == Status.CREATED
    assert "article" in response.json()


def test_유저가_게시글을_저장할_수_있다(로그인_유저1_api):
    payload = {
        "article": {
            **ARTICLE_PAYLOAD["article"],
            "title": "My Test Title",
        }
    }
    response = 로그인_유저1_api.create(payload)
    article = response.json()["article"]

    assert Status.of(response) == Status.CREATED
    assert article["title"] == "My Test Title"


def test_유저가_게시글을_작성하면_slug가_생성된다(로그인_유저1_api):
    payload = {
        "article": {
            **ARTICLE_PAYLOAD["article"],
            "title": "My Test Title",
        }
    }
    response = 로그인_유저1_api.create(payload)
    article = response.json()["article"]

    assert Status.of(response) == Status.CREATED
    assert article["slug"] == "my-test-title"


def test_유저가_게시글을_작성하면_작성자_정보가_저장된다(로그인_유저1_api):
    response = 로그인_유저1_api.create(ARTICLE_PAYLOAD)

    assert Status.of(response) == Status.CREATED
    assert "author" in response.json()["article"]
    assert response.json()["article"]["author"]["username"] == "user1"


def test_로그인하지_않으면_게시글을_작성할_수_없다(게스트_api):
    response = 게스트_api.create(ARTICLE_PAYLOAD)

    assert Status.of(response) == Status.UNAUTHORIZED
