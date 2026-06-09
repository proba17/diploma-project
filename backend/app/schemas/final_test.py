from pydantic import BaseModel


class QuestionRead(BaseModel):
    id: int

    question: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


class AnswerItem(BaseModel):
    question_id: int
    answer: str


class TestSubmit(BaseModel):
    answers: list[AnswerItem]


class TestResultRead(BaseModel):
    score: int
    correct_answers: int
    total_questions: int
    passed: bool

    class Config:
        from_attributes = True