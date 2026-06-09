from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.final_test import TestQuestion
from app.models.final_test import TestResult
from app.models.result import Result

from app.schemas.final_test import QuestionRead
from app.schemas.final_test import TestSubmit
from app.schemas.final_test import TestResultRead
import random
router = APIRouter(
    prefix="/final-test",
    tags=["Final Test"]
)
@router.get(
    "/questions",
    response_model=list[QuestionRead]
)
def get_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    questions = db.query(TestQuestion).all()

    results = (
        db.query(Result)
        .filter(
            Result.user_id == current_user.id
        )
        .all()
    )

    if not results:

        questions_count = 20

    else:

        average_accuracy = round(
            sum(
                (result.accuracy or 0)
                for result in results
            ) / len(results),
            2
        )

        total_false_positives = sum(
            result.false_positives or 0
            for result in results
        )

        if average_accuracy >= 90:
            questions_count = 10

        elif average_accuracy >= 75:
            questions_count = 15

        else:
            questions_count = 20

        if total_false_positives > 20:
            questions_count += 5

    return random.sample(
        questions,
        min(
            questions_count,
            len(questions)
        )
    )
@router.post("/submit")
def submit_test(
    request: TestSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    correct = 0

    for answer in request.answers:

        question = (
            db.query(TestQuestion)
            .filter(
                TestQuestion.id == answer.question_id
            )
            .first()
        )

        if (
            question
            and question.correct_answer == answer.answer
        ):
            correct += 1

    total = len(request.answers)

    score = int(
        correct / total * 100
    )

    passed = score >= 70

    result = TestResult(
        user_id=current_user.id,
        total_questions=total,
        correct_answers=correct,
        score=score,
        passed=passed
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "score": score,
        "correct_answers": correct,
        "total_questions": total,
        "passed": passed
    }

@router.get("/statistics")
def get_final_test_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    results = (
        db.query(TestResult)
        .filter(TestResult.user_id == current_user.id)
        .order_by(TestResult.id.desc())
        .all()
    )

    if not results:
        return {
            "attempts": 0,
            "best_score": 0,
            "average_score": 0,
            "last_score": 0,
            "certificate": "Не получен"
        }

    best_score = max(r.score for r in results)

    average_score = round(
        sum(r.score for r in results) / len(results),
        2
    )

    last_score = results[0].score


    certificate = "Требуется дополнительное обучение"

    if best_score >= 90:
        certificate = "Эксперт сетевой защиты"

    elif best_score >= 80:
        certificate = "Инженер информационной безопасности"

    elif best_score >= 70:
        certificate = "Аналитик SOC"

    return {
        "attempts": len(results),
        "best_score": best_score,
        "average_score": average_score,
        "last_score": last_score,
        "certificate": certificate
    }
@router.get("/difficulty")
def get_test_difficulty(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    results = (
        db.query(Result)
        .filter(
            Result.user_id == current_user.id
        )
        .all()
    )

    if not results:
        return {
            "accuracy": 0,
            "questions_count": 20,
            "level": "Базовый"
        }

    average_accuracy = round(
        sum(
            (result.accuracy or 0)
            for result in results
        ) / len(results),
        2
    )

    total_false_positives = sum(
        result.false_positives or 0
        for result in results
    )

    if average_accuracy >= 90:
        questions_count = 10
        level = "Высокий"

    elif average_accuracy >= 75:
        questions_count = 15
        level = "Средний"

    else:
        questions_count = 20
        level = "Базовый"

    if total_false_positives > 20:
        questions_count += 5

    return {
        "accuracy": average_accuracy,
        "questions_count": questions_count,
        "level": level
    }
