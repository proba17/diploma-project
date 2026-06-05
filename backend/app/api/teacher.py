from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.level import Level
from app.models.result import Result
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/teacher", tags=["Teacher"])


def get_current_teacher_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Teacher access required"
        )

    return current_user


@router.get("/statistics")
def get_teacher_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_user)
):
    users_count = db.query(User).count()
    levels_count = db.query(Level).filter(Level.is_active == True).count()
    results_count = db.query(Result).count()

    completed_levels_count = (
        db.query(Result)
        .filter(Result.completed == 1)
        .count()
    )

    average_score = db.query(func.avg(Result.score)).scalar() or 0
    best_score = db.query(func.max(Result.score)).scalar() or 0

    average_accuracy = db.query(func.avg(Result.accuracy)).scalar() or 0

    total_correct_blocks = db.query(func.sum(Result.correct_blocks)).scalar() or 0
    total_false_positives = db.query(func.sum(Result.false_positives)).scalar() or 0
    total_allowed_normal_traffic = db.query(func.sum(Result.allowed_normal_traffic)).scalar() or 0
    total_damage_taken = db.query(func.sum(Result.damage_taken)).scalar() or 0
    total_time_spent = db.query(func.sum(Result.time_spent)).scalar() or 0

    return {
        "users_count": users_count,
        "levels_count": levels_count,
        "results_count": results_count,
        "completed_levels_count": completed_levels_count,
        "average_score": round(float(average_score), 2),
        "best_score": best_score,
        "average_accuracy": round(float(average_accuracy), 2),
        "total_correct_blocks": total_correct_blocks,
        "total_false_positives": total_false_positives,
        "total_allowed_normal_traffic": total_allowed_normal_traffic,
        "total_damage_taken": total_damage_taken,
        "total_time_spent": total_time_spent,
    }


@router.get("/users")
def get_teacher_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_user)
):
    users = (
        db.query(User)
        .order_by(User.id)
        .all()
    )

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        }
        for user in users
    ]


@router.get("/results")
def get_teacher_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher_user)
):
    results = (
        db.query(Result)
        .order_by(Result.id.desc())
        .all()
    )

    return [
        {
            "id": result.id,
            "user_id": result.user_id,
            "level_id": result.level_id,
            "score": result.score,
            "completed": result.completed,
            "enemies_destroyed": result.enemies_destroyed,
            "damage_taken": result.damage_taken,
            "time_spent": result.time_spent,
            "correct_blocks": result.correct_blocks,
            "false_positives": result.false_positives,
            "allowed_normal_traffic": result.allowed_normal_traffic,
            "accuracy": result.accuracy,
            "created_at": getattr(result, "created_at", None),
        }
        for result in results
    ]