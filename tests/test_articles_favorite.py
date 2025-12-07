"""Articles: Favorite Tests"""


def test_favorite_요청_시_favoritesCount가_증가한다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: favorite 요청
    response = client.post(f"/articles/{slug}/favorite", headers=headers)

    # then: 200 반환 및 favoritesCount 증가
    assert response.status_code == 200
    assert response.json()["article"]["favoritesCount"] == 1
    assert response.json()["article"]["favorited"] == True


def test_unfavorite_요청_시_favoritesCount가_감소한다(client):
    # given: 유저 등록, article 생성, favorite 추가
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # favorite 추가
    client.post(f"/articles/{slug}/favorite", headers=headers)

    # when: unfavorite 요청
    response = client.delete(f"/articles/{slug}/favorite", headers=headers)

    # then: 200 반환 및 favoritesCount 감소
    assert response.status_code == 200
    assert response.json()["article"]["favoritesCount"] == 0
    assert response.json()["article"]["favorited"] == False


def test_토큰_없이_favorite_요청_시_401을_반환한다(client):
    # given: 유저 등록 및 article 생성
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    article_payload = {
        "article": {"title": "Test Article", "description": "Desc", "body": "Body"}
    }
    create_response = client.post("/articles", json=article_payload, headers=headers)
    slug = create_response.json()["article"]["slug"]

    # when: 토큰 없이 favorite 요청
    response = client.post(f"/articles/{slug}/favorite")

    # then: 401 반환
    assert response.status_code == 401

