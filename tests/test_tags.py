from tests.conftest import Status


def test_태그_목록을_조회할_수_있다(로그인_유저1_api):
    # 태그가 있는 글 작성
    payload = {
        "article": {
            "title": "Test Article",
            "description": "Desc",
            "body": "Body",
            "tagList": ["python", "fastapi"],
        }
    }
    로그인_유저1_api.create(payload)

    결과 = 로그인_유저1_api.list_tags()

    assert Status.of(결과) == Status.SUCCESS
    assert "python" in 결과.json()["tags"]
    assert "fastapi" in 결과.json()["tags"]


def test_태그가_없으면_빈_목록을_반환한다(게스트_api):
    결과 = 게스트_api.list_tags()

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["tags"] == []
