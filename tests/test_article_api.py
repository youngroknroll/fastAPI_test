import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

#
pytestmark = pytest.mark.anyio("asyncio")

