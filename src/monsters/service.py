import requests
import random
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.monsters.repository import MonsterRepository
from src.monsters.schemas import MonsterCreate, MonsterUpdate, MonsterFromAPI
from src.monsters.models import Monster


class MonsterService:
    base_url: str = "https://www.dnd5eapi.co"

    def __init__(self, session: AsyncSession):
        self.repository = MonsterRepository(session)

    async def create_monster(self, user_id: int, monster_data: MonsterCreate) -> Monster:
        """Створення монстра для користувача"""
        return await self.repository.create(
            user_id=user_id,
            name=monster_data.name,
            monster_type=monster_data.monster_type,
            challenge_rating=monster_data.challenge_rating,
            hit_points=monster_data.hit_points,
            image_url=monster_data.image_url
        )

    async def get_all_monsters(self, user_id: int) -> List[Monster]:
        """Отримання всіх монстрів користувача"""
        return await self.repository.get_all(user_id)

    async def get_monster_by_id(self, monster_id: int, user_id: int) -> Monster:
        """Отримання монстра за ID"""
        monster = await self.repository.get_by_id(monster_id, user_id)
        if not monster:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Monster not found"
            )
        return monster

    async def update_monster(
            self, monster_id: int, user_id: int, monster_data: MonsterUpdate
    ) -> Monster:
        """Оновлення монстра"""
        monster = await self.get_monster_by_id(monster_id, user_id)

        update_data = monster_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(monster, key, value)

        return await self.repository.update(monster)

    async def delete_monster(self, monster_id: int, user_id: int):
        """Видалення монстра"""
        monster = await self.get_monster_by_id(monster_id, user_id)
        await self.repository.delete(monster)

    async def get_random_monster_from_api(self) -> MonsterFromAPI:
        """Отримання випадкового монстра з D&D API з кешуванням"""
        from src.cache.service import CacheService

        cache_key = "dnd:random_monster"
        cache_service = CacheService()

        # Спроба отримати з кешу
        cached = await cache_service.get(cache_key)
        if cached:
            return MonsterFromAPI(**cached)

        # Якщо немає в кеші - отримуємо з API
        response = requests.get(f"{self.base_url}/api/monsters", timeout=10)
        response.raise_for_status()

        data = response.json()
        monsters = data.get("results", [])

        if not monsters:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No monsters found in D&D API"
            )

        monster = random.choice(monsters)

        detail_response = requests.get(f"{self.base_url}{monster['url']}", timeout=10)
        detail_response.raise_for_status()

        detail_data = detail_response.json()

        image_url = None
        if detail_data.get("image"):
            image_url = f"{self.base_url}{detail_data['image']}"

        result = {
            "name": detail_data["name"],
            "type": detail_data["type"],
            "challenge_rating": detail_data["challenge_rating"],
            "hit_points": detail_data["hit_points"],
            "image_url": image_url
        }

        # Зберігаємо в кеш
        await cache_service.set(cache_key, result)

        return MonsterFromAPI(**result)