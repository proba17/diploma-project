from typing import Any

from pydantic import BaseModel


class LevelBase(BaseModel):
    title: str
    description: str | None = None

    topic: str | None = None
    topic_id: int | None = None

    difficulty: str = "easy"

    base_health: int = 100
    start_resources: int = 100

    map_config: dict[str, Any] | None = None
    waves_config: list[dict[str, Any]] | None = None
    defense_config: list[dict[str, Any]] | None = None
    campaign: str | None = None
    order_number: int = 0


class LevelCreate(LevelBase):
    pass


class LevelUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    topic: str | None = None
    topic_id: int | None = None

    difficulty: str | None = None

    base_health: int | None = None
    start_resources: int | None = None

    map_config: dict[str, Any] | None = None
    waves_config: list[dict[str, Any]] | None = None
    defense_config: list[dict[str, Any]] | None = None

    is_active: bool | None = None

    campaign: str | None = None
    order_number: int | None = None


class LevelRead(LevelBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True