from pydantic import BaseModel


class CacheSetRequest(BaseModel):
    key: str
    value: str


class CacheGetResponse(BaseModel):
    key: str
    value: str | None
