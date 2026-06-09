from pydantic import BaseModel


class DefenseModuleRead(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None
    osi_level: int
    analyzes: list[str]
    blocks: list[str]
    cost: int
    damage: int
    range: int

    class Config:
        from_attributes = True