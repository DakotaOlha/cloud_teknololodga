from unittest.mock import AsyncMock, patch


def test_create_monster(client):
    mock_monster = {"id": 1, "name": "Goblin", "power": 5}

    with patch("src.monsters.router.MonsterService.create_monster",
               new=AsyncMock(return_value=mock_monster)):
        response = client.post("/monsters", json={"name": "Goblin", "power": 5})

    assert response.status_code == 201
    assert response.json()["name"] == "Goblin"


def test_get_all_monsters(client):
    mock_list = [
        {"id": 1, "name": "Goblin", "power": 5},
        {"id": 2, "name": "Orc", "power": 10},
    ]

    with patch("src.monsters.router.MonsterService.get_all_monsters",
               new=AsyncMock(return_value=mock_list)):
        response = client.get("/monsters")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_monster_by_id(client):
    mock_monster = {"id": 1, "name": "Goblin", "power": 5}

    with patch("src.monsters.router.MonsterService.get_monster_by_id",
               new=AsyncMock(return_value=mock_monster)):
        response = client.get("/monsters/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Goblin"


def test_update_monster(client):
    updated = {"id": 1, "name": "Goblin+", "power": 7}

    with patch("src.monsters.router.MonsterService.update_monster",
               new=AsyncMock(return_value=updated)):
        response = client.put("/monsters/1", json={"name": "Goblin+", "power": 7})

    assert response.status_code == 200
    assert response.json()["name"] == "Goblin+"


def test_delete_monster(client):
    with patch("src.monsters.router.MonsterService.delete_monster",
               new=AsyncMock(return_value=True)):
        response = client.delete("/monsters/1")

    assert response.status_code == 204


def test_external_random_monster(client):
    mock_monster = {"name": "Hydra", "power": 20}

    with patch("src.monsters.router.MonsterService.get_random_monster_from_api",
               new=AsyncMock(return_value=mock_monster)):
        response = client.get("/monsters/external/random")

    assert response.status_code == 200
    assert response.json()["name"] == "Hydra"
