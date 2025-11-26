import json
from typing import Any, Optional
from redis import asyncio as aioredis

from src.core.redis_client import get_redis
from src.core.settings import settings


class CacheService:
    def __init__(self):
        self.redis: aioredis.Redis = get_redis()

    async def get(self, key: str) -> Optional[dict]:
        """Отримати значення з кешу"""
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Зберегти значення в кеш"""
        try:
            ttl = ttl or settings.redis_ttl
            serialized = json.dumps(value)
            await self.redis.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"Redis SET error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Видалити значення з кешу"""
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            print(f"Redis DELETE error: {e}")
            return False

    async def close(self):
        """Закрити з'єднання з Redis"""
        await self.redis.close()