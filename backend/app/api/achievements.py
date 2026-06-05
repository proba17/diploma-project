from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.achievement import Achievement, UserAchievement
from app.models.result import Result
from app.models.user import User
from app.schemas.achievement import AchievementRead, UserAchievementRead


router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.get("/", response_model=list[AchievementRead])
def get_achievements(db: Session = Depends(get_db)):
    achievements = db.query(Achievement).order_by(Achievement.id).all()
    return achievements


@router.get("/my", response_model=list[UserAchievementRead])
def get_my_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    achievements = (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == current_user.id)
        .order_by(UserAchievement.earned_at.desc())
        .all()
    )

    return achievements


@router.post("/seed")
def seed_achievements(db: Session = Depends(get_db)):
    existing_achievements = db.query(Achievement).count()

    if existing_achievements > 0:
        return {
            "message": "Achievements already exist",
            "count": existing_achievements
        }

    achievements = [
        Achievement(
            title="Первый шаг",
            description="Пользователь сохранил первый результат прохождения уровня.",
            condition_type="first_result",
            icon="first_step"
        ),
        Achievement(
            title="Первый уровень",
            description="Пользователь успешно прошёл хотя бы один уровень.",
            condition_type="first_completed_level",
            icon="level_complete"
        ),
        Achievement(
            title="Хороший защитник",
            description="Пользователь набрал не менее 800 очков за уровень.",
            condition_type="score_800",
            icon="score_800"
        ),
        Achievement(
            title="Отличный результат",
            description="Пользователь набрал не менее 1000 очков за уровень.",
            condition_type="score_1000",
            icon="score_1000"
        ),
        Achievement(
            title="Минимальный урон",
            description="Пользователь завершил уровень с уроном не более 10.",
            condition_type="low_damage",
            icon="low_damage"
        ),
        Achievement(
            title="Активная защита",
            description="Пользователь уничтожил не менее 50 вредоносных пакетов.",
            condition_type="destroy_50",
            icon="destroy_50"
        ),
    ]

    db.add_all(achievements)
    db.commit()

    return {
        "message": "Achievements created",
        "count": len(achievements)
    }


@router.post("/check")
def check_my_achievements(
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
            "message": "No results yet",
            "new_achievements": []
        }

    all_achievements = db.query(Achievement).all()

    existing_user_achievements = (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == current_user.id)
        .all()
    )

    existing_ids = {
        item.achievement_id for item in existing_user_achievements
    }

    new_achievements = []

    total_destroyed = sum(result.enemies_destroyed for result in results)

    for achievement in all_achievements:
        if achievement.id in existing_ids:
            continue

        earned = False

        if achievement.condition_type == "first_result":
            earned = len(results) >= 1

        elif achievement.condition_type == "first_completed_level":
            earned = any(result.completed == 1 for result in results)

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

        if earned:
            user_achievement = UserAchievement(
                user_id=current_user.id,
                achievement_id=achievement.id
            )

            db.add(user_achievement)

            new_achievements.append({
                "id": achievement.id,
                "title": achievement.title,
                "description": achievement.description,
                "condition_type": achievement.condition_type
            })

    db.commit()

    return {
        "message": "Achievements checked",
        "new_achievements": new_achievements
    }

@router.get("/my/full")
def get_my_achievements_full(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_achievements = (
        db.query(UserAchievement, Achievement)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .filter(UserAchievement.user_id == current_user.id)
        .order_by(UserAchievement.earned_at.desc())
        .all()
    )

    return [
        {
            "id": user_achievement.id,
            "achievement_id": achievement.id,
            "title": achievement.title,
            "description": achievement.description,
            "condition_type": achievement.condition_type,
            "icon": achievement.icon,
            "earned_at": user_achievement.earned_at
        }
        for user_achievement, achievement in user_achievements
    ]