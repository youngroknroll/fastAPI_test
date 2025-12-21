"""Articles: Create Tests"""

def test_로그인한_유저는_게시글을_작성할_수_있다(article_api, user1_header, article_payload):
    response = article_api.create(article_payload, headers=user1_header)

    assert response.status_code == 201
    assert "article" in response.json()


def test_유저가_게시글을_저장할_수_있다(article_api, user1_header, article_payload):
    payload = {
        "article": {
            **article_payload["article"],
            "title": "My Test Title",
        }
    }
    response = article_api.create(payload, headers=user1_header)

    assert response.status_code == 201
    assert response.json()["article"]["title"] == "My Test Title"


def test_유저가_게시글을_작성하면_slug가_생성된다(article_api, user1_header, article_payload):
    payload = {
        "article": {
            **article_payload["article"],
            "title": "My Test Title",
        }
    }
    response = article_api.create(payload, headers=user1_header)

    assert response.status_code == 201
    assert "slug" in response.json()["article"]
    assert response.json()["article"]["slug"] == "my-test-title"


def test_유저가_게시글을_작성하면_작성자_정보가_저장된다(article_api, user1_header, article_payload):
    response = article_api.create(article_payload, headers=user1_header)

    assert response.status_code == 201
    assert "author" in response.json()["article"]
    assert response.json()["article"]["author"]["username"] == "user1"


def test_로그인하지_않으면_게시글을_작성할_수_없다(article_api, article_payload):
    response = article_api.create(article_payload)

    assert response.status_code == 401

