from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.auth import get_current_admin
from app.db.database import get_db
from app.models.level import Level
from app.models.result import Result
from app.models.user import User
from app.api.auth import get_current_user


router = APIRouter(prefix="/admin", tags=["Admin"])


def get_current_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user

class UserRoleUpdate(BaseModel):
    role: str

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    users = db.query(User).order_by(User.id).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.get("/results")
def get_all_results(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    results = (
        db.query(Result)
        .order_by(Result.created_at.desc())
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
            "correct_blocks": result.correct_blocks or 0,
            "false_positives": result.false_positives or 0,
            "allowed_normal_traffic": result.allowed_normal_traffic or 0,
            "accuracy": result.accuracy or 0,
            "created_at": result.created_at
        }
        for result in results
    ]


@router.get("/statistics")
def get_global_statistics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    users_count = db.query(User).count()
    levels_count = db.query(Level).filter(Level.is_active == True).count()
    results = db.query(Result).all()

    if not results:
        return {
            "users_count": users_count,
            "levels_count": levels_count,
            "results_count": 0,
            "completed_levels_count": 0,
            "average_score": 0,
            "best_score": 0,
            "total_enemies_destroyed": 0,
            "total_damage_taken": 0,
            "total_time_spent": 0
        }

    completed_results = [result for result in results if result.completed == 1]

    return {
        "users_count": users_count,
        "levels_count": levels_count,
        "results_count": len(results),
        "completed_levels_count": len(completed_results),
        "average_score": round(
            sum(result.score for result in results) / len(results),
            2
        ),
        "best_score": max(result.score for result in results),
        "total_enemies_destroyed": sum(result.enemies_destroyed for result in results),
        "total_damage_taken": sum(result.damage_taken for result in results),
        "total_time_spent": sum(result.time_spent for result in results)
    }


@router.get("/users/{user_id}/results")
def get_user_results_by_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    results = (
        db.query(Result)
        .filter(Result.user_id == user_id)
        .order_by(Result.created_at.desc())
        .all()
    )

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        "results": [
            {
                "id": result.id,
                "level_id": result.level_id,
                "score": result.score,
                "completed": result.completed,
                "enemies_destroyed": result.enemies_destroyed,
                "damage_taken": result.damage_taken,
                "time_spent": result.time_spent,
                "created_at": result.created_at
            }
            for result in results
        ]
    }


@router.get("/users/{user_id}/statistics")
def get_user_statistics_by_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    results = db.query(Result).filter(Result.user_id == user_id).all()

    if not results:
        return {
            "user_id": user.id,
            "username": user.username,
            "levels_completed": 0,
            "total_score": 0,
            "best_score": 0,
            "average_score": 0,
            "total_enemies_destroyed": 0,
            "total_damage_taken": 0,
            "total_time_spent": 0
        }

    completed_results = [result for result in results if result.completed == 1]

    return {
        "user_id": user.id,
        "username": user.username,
        "levels_completed": len(completed_results),
        "total_score": sum(result.score for result in results),
        "best_score": max(result.score for result in results),
        "average_score": round(
            sum(result.score for result in results) / len(results),
            2
        ),
        "total_enemies_destroyed": sum(result.enemies_destroyed for result in results),
        "total_damage_taken": sum(result.damage_taken for result in results),
        "total_time_spent": sum(result.time_spent for result in results)
    }

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    allowed_roles = ["user", "teacher", "admin"]

    if role_data.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = role_data.role

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }