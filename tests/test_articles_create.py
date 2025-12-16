"""Articles: Create Tests"""

def test_토큰이_있으면_새_article을_작성할_수_있다(client, user1_payload, user1_header, article_payload):
    response = client.post("/articles", json=article_payload, headers=user1_header)

    assert response.status_code == 201
    assert "article" in response.json()


def test_생성된_article은_title을_포함한다(client, user1_payload, user1_header, article_payload):
    payload = {
        "article": {
            **article_payload["article"],
            "title": "My Test Title",
        }
    }
    response = client.post("/articles", json=payload, headers=user1_header)

    assert response.status_code == 201
    assert response.json()["article"]["title"] == "My Test Title"


def test_생성된_article은_slug를_포함한다(client, user1_payload, user1_header, article_payload):
    payload = {
        "article": {
            **article_payload["article"],
            "title": "My Test Title",
        }
    }
    response = client.post("/articles", json=payload, headers=user1_header)

    assert response.status_code == 201
    assert "slug" in response.json()["article"]
    assert response.json()["article"]["slug"] == "my-test-title"


def test_생성된_article은_author_정보를_포함한다(client, user1_payload, user1_header, article_payload):
    response = client.post("/articles", json=article_payload, headers=user1_header)

    assert response.status_code == 201
    assert "author" in response.json()["article"]
    assert response.json()["article"]["author"]["username"] == "user1"


def test_토큰_없이_article_생성_시_401을_반환한다(client, article_payload):
    response = client.post("/articles", json=article_payload)

    assert response.status_code == 401

