from datetime import datetime

from pydantic import BaseModel


class AchievementRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    condition_type: str
    icon: str | None = None

    class Config:
        from_attributes = True


class UserAchievementRead(BaseModel):
    id: int
    user_id: int
    achievement_id: int
    earned_at: datetime

    class Config:
        from_attributes = True