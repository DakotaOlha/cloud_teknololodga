from fastapi import APIRouter, Depends

from src.auth.models import User
from src.auth.service import get_current_user
from src.cache.schemas import CacheGetResponse, CacheSetRequest
from src.cache.service import CacheService

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.post("/set")
async def set_cache(data: CacheSetRequest, current_user: User = Depends(get_current_user)):
    service = CacheService()
    success = await service.set(data.key, data.value)
    return {"success": success, "key": data.key}


@router.get("/get/{key}", response_model=CacheGetResponse)
async def get_cache(key: str, current_user: User = Depends(get_current_user)):
    service = CacheService()
    value = await service.get(key)
    return {"key": key, "value": value}


@router.delete("/delete/{key}")
async def delete_cache(key: str, current_user: User = Depends(get_current_user)):
    service = CacheService()
    success = await service.delete(key)
    return {"success": success, "key": key}
