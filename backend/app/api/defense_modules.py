from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.defense_module import DefenseModule
from app.schemas.defense_module import DefenseModuleRead

router = APIRouter(prefix="/defense-modules", tags=["Defense Modules"])


@router.get("/", response_model=list[DefenseModuleRead])
def get_defense_modules(db: Session = Depends(get_db)):
    return db.query(DefenseModule).order_by(DefenseModule.osi_level).all()


@router.get("/{module_code}", response_model=DefenseModuleRead)
def get_defense_module(module_code: str, db: Session = Depends(get_db)):
    module = db.query(DefenseModule).filter(
        DefenseModule.code == module_code
    ).first()

    if module is None:
        raise HTTPException(status_code=404, detail="Defense module not found")

    return module