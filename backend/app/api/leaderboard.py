from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.result import Result
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/")
def get_leaderboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rows = (
        db.query(
            User.id.label("user_id"),
            User.username.label("username"),
            func.max(Result.score).label("best_score"),
            func.avg(Result.accuracy).label("average_accuracy"),
            func.sum(Result.correct_blocks).label("total_correct_blocks"),
            func.sum(Result.false_positives).label("total_false_positives"),
            func.sum(Result.completed).label("completed_levels"),
        )
        .join(Result, Result.user_id == User.id)
        .group_by(User.id, User.username)
        .order_by(
            func.max(Result.score).desc(),
            func.avg(Result.accuracy).desc()
        )
        .limit(20)
        .all()
    )

    return [
        {
            "place": index + 1,
            "user_id": row.user_id,
            "username": row.username,
            "best_score": row.best_score or 0,
            "average_accuracy": round(float(row.average_accuracy or 0), 2),
            "total_correct_blocks": row.total_correct_blocks or 0,
            "total_false_positives": row.total_false_positives or 0,
            "completed_levels": row.completed_levels or 0,
        }
        for index, row in enumerate(rows)
    ]