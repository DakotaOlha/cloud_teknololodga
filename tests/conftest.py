import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import AsyncMock


class FakeUser:
    def __init__(self):
        self.id = 1
        self.username = "test"
        self.email = "t@t.com"


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def override_current_user(monkeypatch):
    async def fake_user():
        return FakeUser()

    monkeypatch.setattr("src.auth.router.get_current_user", fake_user)
    monkeypatch.setattr("src.monsters.router.get_current_user", fake_user)
    monkeypatch.setattr("src.cache.router.get_current_user", fake_user)


@pytest.fixture
def fake_redis(monkeypatch):
    from fakeredis.aioredis import FakeRedis
    redis = FakeRedis()
    monkeypatch.setattr("src.cache.service.get_redis", lambda: redis)
    return redis
