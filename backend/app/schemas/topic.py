from pydantic import BaseModel


class TopicBase(BaseModel):
    title: str
    short_description: str | None = None
    content: str

    category: str | None = None
    order_number: int = 0


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    title: str | None = None
    short_description: str | None = None
    content: str | None = None

    category: str | None = None
    order_number: int | None = None
    is_active: bool | None = None


class TopicRead(TopicBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True