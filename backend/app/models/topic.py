from sqlalchemy import Boolean, Column, Integer, String, Text

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    short_description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)

    category = Column(String(100), nullable=True)
    order_number = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)