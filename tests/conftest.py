"""Test configuration - imports all fixtures"""

# DB and Client fixtures
from tests.fixtures.db_client_fixtures import session_fixture, client_fixture

# User fixtures
from tests.fixtures.user_fixtures import (
    user1_token,
    user2_token,
    user1_header,
    user2_header,
)

# Article fixtures
from tests.fixtures.article_fixtures import (
    article_payload,
    article_api,
    ArticleAPI,
)

