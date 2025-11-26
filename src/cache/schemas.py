from pydantic import BaseModel
from typing import Any


class CacheSetRequest(BaseModel):
    key: str
    value: str


class CacheGetResponse(BaseModel):
    key: str
    value: str | None