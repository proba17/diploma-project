from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.database import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    topic = Column(String(100), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)

    campaign = Column(String(100), nullable=True)
    order_number = Column(Integer, default=0)

    difficulty = Column(String(30), default="easy")

    base_health = Column(Integer, default=100)
    start_resources = Column(Integer, default=100)

    map_config = Column(JSONB, nullable=True)
    waves_config = Column(JSONB, nullable=True)
    defense_config = Column(JSONB, nullable=True)

    is_active = Column(Boolean, default=True)

    learning_topic = relationship("Topic")