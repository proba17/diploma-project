from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class AttackType(Base):
    __tablename__ = "attack_types"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    osi_level = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    packet_fields = Column(JSONB, nullable=False)
    recommended_modules = Column(JSONB, nullable=False)