"""Articles: Create Tests"""


def test_토큰이_있으면_새_article을_작성할_수_있다(client):
    # given: 유저 등록
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # when: article 생성
    article_payload = {
        "article": {"title": "Test Article", "description": "Test Desc", "body": "Test Body"}
    }
    response = client.post("/articles", json=article_payload, headers=headers)

    # then: 201 반환
    assert response.status_code == 201
    assert "article" in response.json()


def test_생성된_article은_title을_포함한다(client):
    # given: 유저 등록
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # when: article 생성
    article_payload = {
        "article": {"title": "My Test Title", "description": "Test Desc", "body": "Test Body"}
    }
    response = client.post("/articles", json=article_payload, headers=headers)

    # then: title 포함
    assert response.status_code == 201
    assert response.json()["article"]["title"] == "My Test Title"


def test_생성된_article은_slug를_포함한다(client):
    # given: 유저 등록
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # when: article 생성
    article_payload = {
        "article": {"title": "My Test Title", "description": "Test Desc", "body": "Test Body"}
    }
    response = client.post("/articles", json=article_payload, headers=headers)

    # then: slug 포함 (title 기반)
    assert response.status_code == 201
    assert "slug" in response.json()["article"]
    assert response.json()["article"]["slug"] == "my-test-title"


def test_생성된_article은_author_정보를_포함한다(client):
    # given: 유저 등록
    user_payload = {
        "user": {"email": "test@example.com", "password": "password123", "username": "testuser"}
    }
    user_response = client.post("/users", json=user_payload)
    token = user_response.json()["user"]["token"]
    headers = {"Authorization": f"Token {token}"}

    # when: article 생성
    article_payload = {
        "article": {"title": "Test Article", "description": "Test Desc", "body": "Test Body"}
    }
    response = client.post("/articles", json=article_payload, headers=headers)

    # then: author 정보 포함
    assert response.status_code == 201
    assert "author" in response.json()["article"]
    assert response.json()["article"]["author"]["username"] == "testuser"


def test_토큰_없이_article_생성_시_401을_반환한다(client):
    # given: 토큰 없음
    article_payload = {
        "article": {"title": "Test Article", "description": "Test Desc", "body": "Test Body"}
    }

    # when: 토큰 없이 article 생성 시도
    response = client.post("/articles", json=article_payload)

    # then: 401 반환
    assert response.status_code == 401

