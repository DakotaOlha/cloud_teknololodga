from unittest.mock import patch


def test_healthcheck(client):
    response = client.get("/core/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_time(client):
    response = client.get("/core/time")
    assert response.status_code == 200
    assert "server_time" in response.json()


def test_unknown_route_returns_404(client):
    response = client.get("/core/not-existing-route")
    assert response.status_code == 404


def test_healthcheck_wrong_method(client):
    response = client.post("/core/healthcheck")
    assert response.status_code == 405


def test_time_internal_error(client):
    with patch("src.core.router.datetime.datetime") as mock_dt:
        mock_dt.now.side_effect = Exception("Internal error")
        response = client.get("/core/time")
        assert response.status_code == 500