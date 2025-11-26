from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.monsters.models import Monster


class MonsterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        name: str,
        monster_type: str,
        challenge_rating: float,
        hit_points: int,
        image_url: Optional[str] = None,
    ) -> Monster:
        monster = Monster(
            user_id=user_id,
            name=name,
            monster_type=monster_type,
            challenge_rating=challenge_rating,
            hit_points=hit_points,
            image_url=image_url,
        )
        self.session.add(monster)
        await self.session.commit()
        await self.session.refresh(monster)
        return monster

    async def get_all(self, user_id: int) -> List[Monster]:
        result = await self.session.execute(select(Monster).where(Monster.user_id == user_id))
        return list(result.scalars().all())

    async def get_by_id(self, monster_id: int, user_id: int) -> Optional[Monster]:
        result = await self.session.execute(select(Monster).where(Monster.id == monster_id, Monster.user_id == user_id))
        return result.scalar_one_or_none()

    async def update(self, monster: Monster) -> Monster:
        await self.session.commit()
        await self.session.refresh(monster)
        return monster

    async def delete(self, monster: Monster):
        await self.session.delete(monster)
        await self.session.commit()
