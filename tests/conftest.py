from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.auth.service import get_current_user
from src.main import app


class FakeUser:
    def __init__(self):
        self.id = 1
        self.username = "test"
        self.email = "t@t.com"
        self.is_active = True
        self.created_at = datetime(2024, 1, 1)
        self.updated_at = datetime(2024, 1, 1)


@pytest.fixture(scope="function")
def client():
    app.dependency_overrides.clear()

    async def fake_current_user():
        return FakeUser()

    app.dependency_overrides[get_current_user] = fake_current_user

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def fake_redis(monkeypatch):
    from fakeredis.aioredis import FakeRedis

    redis = FakeRedis()
    monkeypatch.setattr("src.cache.service.get_redis", lambda: redis)
    return redis
