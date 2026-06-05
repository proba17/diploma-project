from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    score = Column(Integer, nullable=False)
    completed = Column(Integer, default=1)

    enemies_destroyed = Column(Integer, default=0)
    damage_taken = Column(Integer, default=0)
    time_spent = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    correct_blocks = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    allowed_normal_traffic = Column(Integer, default=0)
    accuracy = Column(Integer, default=0)
    correct_blocks = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    allowed_normal_traffic = Column(Integer, default=0)
    accuracy = Column(Integer, default=0)