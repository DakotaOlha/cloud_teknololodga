from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class MonsterCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    monster_type: str = Field(..., min_length=1, max_length=100)
    challenge_rating: float = Field(..., ge=0)
    hit_points: int = Field(..., ge=1)
    image_url: Optional[str] = None


class MonsterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    monster_type: Optional[str] = Field(None, min_length=1, max_length=100)
    challenge_rating: Optional[float] = Field(None, ge=0)
    hit_points: Optional[int] = Field(None, ge=1)
    image_url: Optional[str] = None


class MonsterResponse(BaseModel):
    id: int
    user_id: int
    name: str
    monster_type: str
    challenge_rating: float
    hit_points: int
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MonsterFromAPI(BaseModel):
    name: str
    type: str
    challenge_rating: float
    hit_points: int
    image_url: Optional[str] = None