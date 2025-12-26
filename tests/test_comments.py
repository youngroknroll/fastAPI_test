from tests.conftest import ARTICLE_PAYLOAD, Status


def test_게시글에_댓글을_작성할_수_있다(로그인_유저1_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]

    결과 = 로그인_유저1_api.create_comment(slug, "This is a comment")

    assert Status.of(결과) == Status.SUCCESS
    assert 결과.json()["comment"]["body"] == "This is a comment"
    assert "id" in 결과.json()["comment"]
    assert "author" in 결과.json()["comment"]


def test_로그인하지_않으면_댓글을_작성할_수_없다(로그인_유저1_api, 게스트_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]

    결과 = 게스트_api.create_comment(slug, "This is a comment")

    assert Status.of(결과) == Status.UNAUTHORIZED


def test_게시글의_댓글_목록을_조회할_수_있다(로그인_유저1_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]
    로그인_유저1_api.create_comment(slug, "First comment")

    결과 = 로그인_유저1_api.list_comments(slug)

    assert Status.of(결과) == Status.SUCCESS
    assert len(결과.json()["comments"]) == 1
    assert 결과.json()["comments"][0]["body"] == "First comment"


def test_자신의_댓글을_삭제할_수_있다(로그인_유저1_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]
    댓글 = 로그인_유저1_api.create_comment(slug, "Comment to delete").json()["comment"]
    comment_id = 댓글["id"]

    삭제_결과 = 로그인_유저1_api.delete_comment(slug, comment_id)

    assert Status.of(삭제_결과) == Status.DELETED

    # 댓글이 삭제되었는지 확인
    조회_결과 = 로그인_유저1_api.list_comments(slug)
    assert len(조회_결과.json()["comments"]) == 0


def test_다른_사람의_댓글은_삭제할_수_없다(로그인_유저1_api, 로그인_유저2_api):
    작성된_글 = 로그인_유저1_api.create(ARTICLE_PAYLOAD).json()["article"]
    slug = 작성된_글["slug"]
    댓글 = 로그인_유저1_api.create_comment(slug, "User1's comment").json()["comment"]
    comment_id = 댓글["id"]

    삭제_결과 = 로그인_유저2_api.delete_comment(slug, comment_id)

    assert Status.of(삭제_결과) == Status.FORBIDDEN
