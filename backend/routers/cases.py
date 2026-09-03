"""SUTRA Backend — routers/cases.py : case management endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from auth import require_role, TokenData
from database import get_db
import models

router = APIRouter()

class CaseCreate(BaseModel):
    title: str
    description: str = ""
    jurisdiction: Optional[str] = None
    sensitivity: str = "standard"

class CaseResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: str
    jurisdiction: Optional[str] = None
    sensitivity: str
    created_at: datetime
    created_by_username: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

@router.post("", response_model=CaseResponse)
def create_case(payload: CaseCreate, user: TokenData = Depends(require_role("investigator")), db: Session = Depends(get_db)):
    # Find user
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found in DB")
    
    # Generate Case ID (simple sequence alternative)
    count = db.query(models.Case).count()
    case_id = f"CASE-{count + 1:04d}"

    new_case = models.Case(
        id=case_id,
        title=payload.title,
        description=payload.description,
        jurisdiction=payload.jurisdiction,
        sensitivity=payload.sensitivity,
        created_by_id=db_user.id
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    
    # Prepare response
    response = CaseResponse.from_orm(new_case)
    response.created_by_username = db_user.username
    return response

@router.get("", response_model=List[CaseResponse])
def list_cases(user: TokenData = Depends(require_role("analyst")), db: Session = Depends(get_db)):
    cases = db.query(models.Case).all()
    results = []
    for c in cases:
        resp = CaseResponse.from_orm(c)
        if c.created_by:
            resp.created_by_username = c.created_by.username
        results.append(resp)
    return results

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, user: TokenData = Depends(require_role("analyst")), db: Session = Depends(get_db)):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    resp = CaseResponse.from_orm(case)
    if case.created_by:
        resp.created_by_username = case.created_by.username
    return resp
