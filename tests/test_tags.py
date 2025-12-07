"""Tags Tests"""


def test_GET_tags_요청_시_문자열_배열을_반환한다(client):
    # given: 유저 등록 및 태그가 있는 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {
            "title": "Test Article",
            "description": "Desc",
            "body": "Body",
            "tagList": ["python", "fastapi"],
        }
    }
    client.post("/articles", json=article_payload, headers=headers)

    # when: tags 조회
    response = client.get("/tags")

    # then: 200 반환 및 tags 배열 포함
    assert response.status_code == 200
    assert "tags" in response.json()
    assert isinstance(response.json()["tags"], list)
    assert "python" in response.json()["tags"]
    assert "fastapi" in response.json()["tags"]


def test_tag가_없으면_빈_배열을_반환한다(client):
    # when: tags 조회 (아무 article도 없음)
    response = client.get("/tags")

    # then: 200 반환 및 빈 배열
    assert response.status_code == 200
    assert response.json()["tags"] == []

