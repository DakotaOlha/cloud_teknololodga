from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.database import get_db
from src.auth.service import get_current_user
from src.auth.models import User
from src.monsters.service import MonsterService
from src.monsters.schemas import (
    MonsterCreate,
    MonsterUpdate,
    MonsterResponse,
    MonsterFromAPI
)

router = APIRouter(prefix="/monsters", tags=["Monsters"])


@router.post("", response_model=MonsterResponse, status_code=status.HTTP_201_CREATED)
async def create_monster(
    monster_data: MonsterCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Створити нового монстра"""
    service = MonsterService(session)
    return await service.create_monster(current_user.id, monster_data)


@router.get("", response_model=List[MonsterResponse])
async def get_all_monsters(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Отримати всіх монстрів користувача"""
    service = MonsterService(session)
    return await service.get_all_monsters(current_user.id)


@router.get("/{monster_id}", response_model=MonsterResponse)
async def get_monster(
    monster_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Отримати монстра за ID"""
    service = MonsterService(session)
    return await service.get_monster_by_id(monster_id, current_user.id)


@router.put("/{monster_id}", response_model=MonsterResponse)
async def update_monster(
    monster_id: int,
    monster_data: MonsterUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Оновити монстра"""
    service = MonsterService(session)
    return await service.update_monster(monster_id, current_user.id, monster_data)


@router.delete("/{monster_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monster(
    monster_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Видалити монстра"""
    service = MonsterService(session)
    await service.delete_monster(monster_id, current_user.id)


@router.get("/external/random", response_model=MonsterFromAPI)
async def get_random_monster_from_api(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Отримати випадкового монстра з D&D API"""
    service = MonsterService(session)
    return await service.get_random_monster_from_api()  # Додали await