from unittest.mock import AsyncMock, patch


def test_create_monster(client):
    mock_monster_data = {
        "id": 1,
        "name": "Goblin",
        "power": 5,
        "user_id": 1,
        "monster_type": "humanoid",
        "challenge_rating": 1.0,
        "hit_points": 10,
        "image_url": "http://example.com/goblin.png",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }

    with patch("src.monsters.router.MonsterService.create_monster", new=AsyncMock(return_value=mock_monster_data)):
        response = client.post(
            "/monsters",
            json={"name": "Goblin", "power": 5, "monster_type": "humanoid", "challenge_rating": 1.0, "hit_points": 10},
        )

    assert response.status_code == 201


def test_get_all_monsters(client):
    mock_list = [
        {
            "id": 1,
            "name": "Goblin",
            "power": 5,
            "user_id": 1,
            "monster_type": "humanoid",
            "challenge_rating": 1.0,
            "hit_points": 10,
            "image_url": "http://example.com/goblin.png",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }
    ]

    with patch("src.monsters.router.MonsterService.get_all_monsters", new=AsyncMock(return_value=mock_list)):
        response = client.get("/monsters")

    assert response.status_code == 200


def test_external_random_monster(client):
    mock_monster = {"name": "Hydra", "power": 20, "type": "dragon", "challenge_rating": 10.0, "hit_points": 100}

    with patch(
        "src.monsters.router.MonsterService.get_random_monster_from_api", new=AsyncMock(return_value=mock_monster)
    ):
        response = client.get("/monsters/external/random")

    assert response.status_code == 200
