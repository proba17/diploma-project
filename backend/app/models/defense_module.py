from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.db.database import Base


class DefenseModule(Base):
    __tablename__ = "defense_modules"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    osi_level = Column(Integer, nullable=False)

    analyzes = Column(JSONB, nullable=False)
    blocks = Column(JSONB, nullable=False)

    cost = Column(Integer, default=100)
    damage = Column(Integer, default=1)
    range = Column(Integer, default=120)