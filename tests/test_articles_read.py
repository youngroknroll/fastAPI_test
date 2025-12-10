"""Articles: Read Tests"""


def test_GET_articles_호출_시_articles_배열을_반환한다(client):
    # when: GET /articles 호출
    response = client.get("/articles")

    # then: articlesCount를 반환
    assert response.status_code == 200
    data = response.json()
    assert "articlesCount" in data
    assert isinstance(data["articlesCount"], int)


def test_단일_article_조회_시_slug에_해당하는_article을_반환한다(client):
    # given: 유저를 등록하고 article 생성
    register_payload = {
        "user": {
            "email": "author@example.com",
            "password": "password123",
            "username": "author",
        }
    }
    register_response = client.post("/users", json=register_payload)
    token = register_response.json()["user"]["token"]

    # article 생성
    headers = {"Authorization": f"Token {token}"}
    article_payload = {
        "article": {
            "title": "Test Article",
            "description": "Test Description",
            "body": "Test Body",
        }
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: slug로 article 조회
    response = client.get(f"/articles/{slug}")

    # then: article 객체를 반환
    assert response.status_code == 200
    data = response.json()
    assert "article" in data
    assert data["article"]["slug"] == slug


def test_존재하지_않는_slug이면_404를_반환한다(client):
    # when: 존재하지 않는 slug로 article 조회
    response = client.get("/articles/nonexistent-slug")

    # then: 404 반환
    assert response.status_code == 404

