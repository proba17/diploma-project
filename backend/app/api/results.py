from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.achievement import Achievement, UserAchievement
from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.level import Level
from app.models.result import Result
from app.models.user import User
from app.schemas.result import ResultCreate, ResultRead


router = APIRouter(prefix="/results", tags=["Results"])

def check_and_give_achievements(
    db: Session,
    user_id: int
):
    results = (
        db.query(Result)
        .filter(Result.user_id == user_id)
        .all()
    )

    if not results:
        return []

    all_achievements = db.query(Achievement).all()

    existing_user_achievements = (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == user_id)
        .all()
    )

    existing_ids = {
        item.achievement_id for item in existing_user_achievements
    }

    new_achievements = []

    total_destroyed = sum(result.enemies_destroyed for result in results)
    total_completed = sum(1 for result in results if result.completed == 1)

    for achievement in all_achievements:
        if achievement.id in existing_ids:
            continue

        earned = False

        if achievement.condition_type == "first_result":
            earned = len(results) >= 1

        elif achievement.condition_type == "first_completed_level":
            earned = total_completed >= 1

        elif achievement.condition_type == "score_800":
            earned = any(result.score >= 800 for result in results)

        elif achievement.condition_type == "score_1000":
            earned = any(result.score >= 1000 for result in results)

        elif achievement.condition_type == "low_damage":
            earned = any(
                result.completed == 1 and result.damage_taken <= 10
                for result in results
            )

        elif achievement.condition_type == "destroy_50":
            earned = total_destroyed >= 50

        elif achievement.condition_type == "complete_3_levels":
            earned = total_completed >= 3

        elif achievement.condition_type == "destroy_100":
            earned = total_destroyed >= 100

        if earned:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id
            )

            db.add(user_achievement)

            new_achievements.append({
                "id": achievement.id,
                "title": achievement.title,
                "description": achievement.description,
                "condition_type": achievement.condition_type
            })

    return new_achievements

@router.post("/", response_model=ResultRead)
def create_result(
    result_data: ResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    level = (
        db.query(Level)
        .filter(Level.id == result_data.level_id, Level.is_active == True)
        .first()
    )

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )

    result = Result(
        user_id=current_user.id,
        level_id=result_data.level_id,
        score=result_data.score,
        completed=result_data.completed,
        enemies_destroyed=result_data.enemies_destroyed,
        damage_taken=result_data.damage_taken,
        time_spent=result_data.time_spent,

        correct_blocks=result_data.correct_blocks,
        false_positives=result_data.false_positives,
        allowed_normal_traffic=result_data.allowed_normal_traffic,
        accuracy=result_data.accuracy,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    new_achievements = check_and_give_achievements(
        db=db,
        user_id=current_user.id
    )

    db.commit()

    return result


@router.get("/my", response_model=list[ResultRead])
def get_my_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .order_by(Result.created_at.desc())
        .all()
    )

    total_correct_blocks = sum(result.correct_blocks for result in results)
    total_false_positives = sum(result.false_positives for result in results)
    total_allowed_normal_traffic = sum(result.allowed_normal_traffic for result in results)

    average_accuracy = 0

    if results:
        average_accuracy = round(
            sum(result.accuracy for result in results) / len(results),
            2
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

            "created_at": result.created_at,
        }
        for result in results
    ]


@router.get("/my/best", response_model=list[ResultRead])
def get_my_best_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    all_results = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .order_by(Result.level_id, Result.score.desc())
        .all()
    )

    best_results_by_level = {}

    for result in all_results:
        if result.level_id not in best_results_by_level:
            best_results_by_level[result.level_id] = result

    return list(best_results_by_level.values())


@router.get("/statistics")
def get_my_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .all()
    )

    if not results:
        return {
            "levels_completed": 0,
            "total_score": 0,
            "best_score": 0,
            "total_enemies_destroyed": 0,
            "total_damage_taken": 0,
            "total_time_spent": 0
        }

    completed_results = [result for result in results if result.completed == 1]

    total_correct_blocks = sum(
        result.correct_blocks or 0
        for result in results
    )

    total_false_positives = sum(
        result.false_positives or 0
        for result in results
    )

    total_allowed_normal_traffic = sum(
        result.allowed_normal_traffic or 0
        for result in results
    )

    average_accuracy = 0

    if results:
        average_accuracy = round(
            sum((result.accuracy or 0) for result in results) / len(results),
            2
        )
    return {
        "levels_completed": len(completed_results),
        "total_score": sum(result.score for result in results),
        "best_score": max(result.score for result in results),
        "total_enemies_destroyed": sum(result.enemies_destroyed for result in results),
        "total_damage_taken": sum(result.damage_taken for result in results),
        "total_time_spent": sum(result.time_spent for result in results),
        "total_correct_blocks": total_correct_blocks,
        "total_false_positives": total_false_positives,
        "total_allowed_normal_traffic": total_allowed_normal_traffic,
        "average_accuracy": average_accuracy,
    }