from pydantic import BaseModel
from typing import Optional, Any, Dict


class PacketTemplateOut(BaseModel):
    id: int
    name: str
    protocol: str
    src_ip: Optional[str]
    dst_ip: Optional[str]
    src_port: Optional[int]
    dst_port: Optional[int]
    application_protocol: Optional[str]
    domain: Optional[str]
    payload: Optional[str]
    signature: Optional[str]
    attack_type: Optional[str]
    osi_level: int
    is_malicious: bool
    metadata_json: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True