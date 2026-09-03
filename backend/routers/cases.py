"""SUTRA Backend — routers/cases.py : case management endpoints."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from auth import require_role, TokenData

router = APIRouter()


class CaseCreate(BaseModel):
    title: str
    description: str = ""


class Case(CaseCreate):
    case_id: str
    created_by: str
    created_at: datetime
    status: str = "active"


# In production this is a PostgreSQL table (see database/models.py). Kept
# in-memory here so the API is runnable/demoable without a DB connection.
_CASES: dict[str, Case] = {}
_counter = 0


@router.post("", response_model=Case)
def create_case(payload: CaseCreate, user: TokenData = Depends(require_role("investigator"))):
    global _counter
    _counter += 1
    case_id = f"CASE-{_counter:04d}"
    case = Case(case_id=case_id, created_by=user.username, created_at=datetime.utcnow(), **payload.dict())
    _CASES[case_id] = case
    return case


@router.get("")
def list_cases(user: TokenData = Depends(require_role("analyst"))):
    return list(_CASES.values())


@router.get("/{case_id}")
def get_case(case_id: str, user: TokenData = Depends(require_role("analyst"))):
    return _CASES.get(case_id, {"error": "case not found"})
