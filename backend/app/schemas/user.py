from pydantic import BaseModel, EmailStr

from datetime import datetime
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

        class TestResultCreate(BaseModel):
            test_id: str
            test_title: str
            correct_answers: int
            total_questions: int
            percent: int

        class TestResultRead(TestResultCreate):
            id: int
            user_id: int
            created_at: datetime

            class Config:
                from_attributes = True
