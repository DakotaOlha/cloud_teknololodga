from unittest.mock import patch, AsyncMock
from src.auth.schemas import UserResponse


class FakeUser:
    id = 1
    username = "test"
    email = "t@t.com"


def test_register_success(client):
    mock_user = {
        "id": 1,
        "username": "test",
        "email": "t@t.com",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }

    with patch("src.auth.router.AuthService.register_user",
               new=AsyncMock(return_value=mock_user)):
        response = client.post("/auth/register", json={
            "username": "test",
            "email": "t@t.com",
            "password": "12345"
        })

    assert response.status_code == 201
    assert response.json()["username"] == "test"


def test_register_error(client):
    with patch("src.auth.router.AuthService.register_user",
               new=AsyncMock(side_effect=Exception("fail"))):
        response = client.post("/auth/register", json={
            "username": "test",
            "email": "t@t.com",
            "password": "123456"
        })

    assert response.status_code == 500


def test_login_success(client):
    fake_user = FakeUser()

    with patch("src.auth.router.AuthService.authenticate_user",
               new=AsyncMock(return_value=fake_user)):
        with patch("src.auth.router.AuthService.create_access_token",
                   return_value="token123"):
            response = client.post("/auth/login", data={
                "username": "test",
                "password": "123"
            })

    assert response.status_code == 200
    assert response.json()["access_token"] == "token123"


def test_login_invalid_credentials(client):
    with patch("src.auth.router.AuthService.authenticate_user",
               new=AsyncMock(return_value=None)):
        response = client.post("/auth/login", data={
            "username": "wrong",
            "password": "wrong"
        })

    assert response.status_code == 401


def test_me_success(client):
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert "username" in response.json()
