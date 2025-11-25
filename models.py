from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import List, Optional


class DndMonster(BaseModel):
    index: str
    name: str
    url: str

    model_config = ConfigDict(extra="ignore")


class DndMonsterDetail(BaseModel):
    index: str
    name: str
    size: str
    type: str
    alignment: str
    armor_class: List[dict] = []
    hit_points: int
    challenge_rating: float
    image: Optional[str] = Field(default=None)
    url: str

    model_config = ConfigDict(extra="ignore")


class DndCombined(BaseModel):
    name: str
    type: str
    challenge_rating: float
    hit_points: int
    image_url: Optional[str] = None

    model_config: ConfigDict = ConfigDict(from_attributes=True)