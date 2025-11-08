import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.core.db import get_session


@pytest.fixture
def client(session: Session):
    """
    테스트용 클라이언트 생성
    conftest.py의 session을 주입받아 FastAPI 앱의 DB를 테스트 DB로 교체
    """

    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


# ============================================
# 조회 테스트
# ============================================


def test_빈_목록_조회(client):
    """게시글이 없을 때 빈 리스트 반환"""
    # when: 목록 조회
    response = client.get("/articles")

    # then: 빈 리스트
    assert response.status_code == 200
    assert response.json() == []


def test_게시글_목록_조회(client):
    """게시글이 있을 때 전체 목록 반환"""
    # given: 게시글 2개 생성
    client.post("/articles", json={"title": "첫 번째 글", "author": "홍길동"})
    client.post("/articles", json={"title": "두 번째 글", "author": "김철수"})

    # when: 목록 조회
    response = client.get("/articles")

    # then: 2개의 게시글 반환
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 2
    assert articles[0]["title"] == "첫 번째 글"
    assert articles[1]["title"] == "두 번째 글"


def test_게시글_단건_조회_성공(client):
    """존재하는 게시글 조회"""
    # given: 게시글 생성
    created = client.post(
        "/articles", json={"title": "테스트 글", "author": "작성자"}
    ).json()

    # when: ID로 조회
    response = client.get(f"/articles/{created['id']}")

    # then: 게시글 정보 반환
    assert response.status_code == 200
    article = response.json()
    assert article["id"] == created["id"]
    assert article["title"] == "테스트 글"
    assert article["author"] == "작성자"


def test_게시글_단건_조회_실패_존재하지_않는_ID(client):
    """존재하지 않는 게시글 조회 시 404"""
    # when: 존재하지 않는 ID로 조회
    response = client.get("/articles/999")

    # then: 404 에러
    assert response.status_code == 404


# ============================================
# 생성 테스트
# ============================================


def test_게시글_생성_성공(client):
    """게시글 생성"""
    # given: 게시글 데이터
    payload = {"title": "새 게시글", "author": "작성자"}

    # when: 생성 요청
    response = client.post("/articles", json=payload)

    # then: 201 상태코드와 생성된 데이터 반환
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == "새 게시글"
    assert created["author"] == "작성자"
    assert created["id"] is not None


# ============================================
# 수정 테스트
# ============================================


def test_게시글_수정_성공(client):
    """게시글 수정"""
    # given: 게시글 생성
    created = client.post(
        "/articles", json={"title": "원본 제목", "author": "원본 작성자"}
    ).json()

    # when: 수정 요청
    response = client.put(
        f"/articles/{created['id']}",
        json={"title": "수정된 제목", "author": "수정된 작성자"},
    )

    # then: 수정된 데이터 반환
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == created["id"]
    assert updated["title"] == "수정된 제목"
    assert updated["author"] == "수정된 작성자"


def test_게시글_수정_실패_존재하지_않는_ID(client):
    """존재하지 않는 게시글 수정 시 404"""
    # when: 존재하지 않는 ID로 수정 시도
    response = client.put("/articles/999", json={"title": "수정", "author": "작성자"})

    # then: 404 에러
    assert response.status_code == 404


# ============================================
# 삭제 테스트
# ============================================


def test_게시글_삭제_성공(client):
    """게시글 삭제"""
    # given: 게시글 생성
    created = client.post(
        "/articles", json={"title": "삭제할 글", "author": "작성자"}
    ).json()

    # when: 삭제 요청
    response = client.delete(f"/articles/{created['id']}")

    # then: 204 상태코드
    assert response.status_code == 204

    # and: 삭제 확인 - 조회 시 404
    get_response = client.get(f"/articles/{created['id']}")
    assert get_response.status_code == 404


def test_게시글_삭제_실패_존재하지_않는_ID(client):
    """존재하지 않는 게시글 삭제 시 404"""
    # when: 존재하지 않는 ID로 삭제 시도
    response = client.delete("/articles/999")

    # then: 404 에러
    assert response.status_code == 404


# ============================================
# 통합 시나리오 테스트
# ============================================


def test_게시글_전체_시나리오(client):
    """생성 → 조회 → 수정 → 삭제 전체 흐름"""
    # 1. 생성
    created = client.post(
        "/articles", json={"title": "시나리오 테스트", "author": "테스터"}
    ).json()
    article_id = created["id"]

    # 2. 조회 확인
    get_response = client.get(f"/articles/{article_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "시나리오 테스트"

    # 3. 수정
    update_response = client.put(
        f"/articles/{article_id}", json={"title": "수정됨", "author": "테스터"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "수정됨"

    # 4. 목록에서 확인
    list_response = client.get("/articles")
    assert len(list_response.json()) == 1

    # 5. 삭제
    delete_response = client.delete(f"/articles/{article_id}")
    assert delete_response.status_code == 204

    # 6. 삭제 확인
    final_get = client.get(f"/articles/{article_id}")
    assert final_get.status_code == 404

    # 7. 목록이 비었는지 확인
    final_list = client.get("/articles")
    assert final_list.json() == []
