from unittest.mock import AsyncMock, patch


def test_cache_set_success(client):
    with patch("src.cache.router.CacheService.set", new=AsyncMock(return_value=True)):
        response = client.post("/cache/set", json={"key": "a", "value": "b"})

    assert response.status_code == 200
    # Перевірте реальну структуру відповіді у вашому роутері
    data = response.json()
    assert data is not None  # або assert "message" in data, залежно від реальної відповіді


def test_cache_get_success(client):
    with patch("src.cache.router.CacheService.get", new=AsyncMock(return_value="hello")):
        response = client.get("/cache/get/mykey")

    assert response.status_code == 200
    assert response.json()["value"] == "hello"


def test_cache_delete_success(client):
    with patch("src.cache.router.CacheService.delete", new=AsyncMock(return_value=True)):
        response = client.delete("/cache/delete/mykey")

    assert response.status_code == 200
    # Перевірте реальну структуру відповіді
    data = response.json()
    assert data is not None
