from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_articles_list():
    # given 서버가 실행 중이고 /articles/{id} 엔드포인트가 존재할 때

    # when 클라이언트가 /articles/1 로 GET 요청을 보낸다
    response = client.get("/articles")

    # then 200 코드와 함께 해당 아티클의 title 과 author 를 응답한다
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("title" in article for article in data)

def test_get_articles_by_id():
    #given 서버가 실행중이며 /articles/{id} 엔드포인트가 존재
    #when 클라이언트가 /articles/1로 GET 요청
    response = client.get("/articles/1")
    #then 200코드와 해당 아티클의 title 및 author 응답
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "author" in data