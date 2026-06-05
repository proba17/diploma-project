from pydantic import BaseModel


class ResultCreate(BaseModel):
    level_id: int
    score: int
    completed: int = 1
    enemies_destroyed: int = 0
    damage_taken: int = 0
    time_spent: int = 0
    correct_blocks: int = 0
    false_positives: int = 0
    allowed_normal_traffic: int = 0
    accuracy: int = 0


class ResultRead(BaseModel):
    id: int
    user_id: int
    level_id: int
    score: int
    completed: int
    enemies_destroyed: int
    damage_taken: int
    time_spent: int

    class Config:
        from_attributes = True

    correct_blocks: int = 0
    false_positives: int = 0
    allowed_normal_traffic: int = 0
    accuracy: int = 0