from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.db.database import Base


class PacketTemplate(Base):
    __tablename__ = "packet_templates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    protocol = Column(String, nullable=False)

    src_ip = Column(String)
    dst_ip = Column(String)

    src_port = Column(Integer)
    dst_port = Column(Integer)

    application_protocol = Column(String)
    domain = Column(String)

    payload = Column(Text)
    signature = Column(String)
    attack_type = Column(String)

    osi_level = Column(Integer, nullable=False)
    is_malicious = Column(Boolean, default=False)

    metadata_json = Column(JSONB, default={})