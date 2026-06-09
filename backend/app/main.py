from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import defense_modules
from app.api import achievements, admin, auth, levels, results, topics
from app.db.database import Base, engine
from app.models.achievement import Achievement, UserAchievement
from app.models.level import Level
from app.models.result import Result
from app.models.topic import Topic
from app.models.user import User
from app.api import teacher
from app.api import leaderboard
from app.models.defense_module import DefenseModule
from app.models.packet_template import PacketTemplate
from app.models.final_test import TestQuestion, TestResult
from app.api import final_test
from app.db.database import SessionLocal
from app.db.seed_defense_modules import seed_defense_modules
from app.db.seed_test_questions import seed_questions
from app.db.database import SessionLocal
app = FastAPI(
    title="CyberDefense Game API",
    description="Backend API для дипломного проекта обучающей игры Tower Defense",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(levels.router)
app.include_router(results.router)
app.include_router(topics.router)
app.include_router(admin.router)
app.include_router(achievements.router)
app.include_router(teacher.router)
app.include_router(leaderboard.router)
app.include_router(defense_modules.router)
app.include_router(final_test.router)
@app.on_event("startup")
def startup():

    db = SessionLocal()

    try:
        seed_questions(db)
    finally:
        db.close()
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running"
    }

app.include_router(
    final_test.router
)
