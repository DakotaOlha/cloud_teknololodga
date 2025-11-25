import requests
import random
from typing import List
from models import DndMonster, DndMonsterDetail, DndCombined


class DndService:
    base_url: str = "https://www.dnd5eapi.co"

    def get_random_monster(self) -> DndCombined:

        response = requests.get(f"{self.base_url}/api/monsters", timeout=10)
        response.raise_for_status()

        data = response.json()
        monsters = [DndMonster(**m) for m in data.get("results", [])]

        if not monsters:
            raise ValueError("No monsters found.")

        monster = random.choice(monsters)

        detail_response = requests.get(
            f"{self.base_url}{monster.url}",
            timeout=10
        )
        detail_response.raise_for_status()

        detail_data = detail_response.json()
        monster_detail = DndMonsterDetail(**detail_data)

        image_url = None
        if monster_detail.image:
            image_url = f"{self.base_url}{monster_detail.image}"

        return DndCombined(
            name=monster_detail.name,
            type=monster_detail.type,
            challenge_rating=monster_detail.challenge_rating,
            hit_points=monster_detail.hit_points,
            image_url=image_url
        )

    def get_all_monster_names(self) -> List[str]:

        response = requests.get(f"{self.base_url}/api/monsters", timeout=10)
        response.raise_for_status()

        data = response.json()
        monsters = [DndMonster(**m) for m in data.get("results", [])]

        return [monster.name for monster in monsters]


service = DndService()