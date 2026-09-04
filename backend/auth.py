"""
SUTRA Backend — auth.py
==========================
JWT authentication + role-based access control (RBAC), per blueprint
Part 17. Roles: admin, senior_investigator, investigator, analyst, viewer.
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from database import SessionLocal
from models import User

SECRET_KEY = os.environ.get("SUTRA_JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)
router = APIRouter()

# Role hierarchy — used by require_role() to check "at least this level"
ROLE_LEVELS = {"viewer": 0, "analyst": 1, "investigator": 2, "senior_investigator": 3, "admin": 4}

class TokenData(BaseModel):
    username: str
    role: str

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    # Prototype/Mockup Bypass: Always return a valid admin user without checking tokens
    # so the frontend can easily pull all data without logging in first.
    return TokenData(username="demo_investigator", role="admin")

def require_role(min_role: str):
    """Dependency factory: require_role('investigator') blocks viewers/analysts."""
    def checker(user: TokenData = Depends(get_current_user)):
        if ROLE_LEVELS.get(user.role, -1) < ROLE_LEVELS.get(min_role, 99):
            raise HTTPException(status_code=403, detail=f"Requires role '{min_role}' or higher")
        return user
    return checker

from database import SessionLocal
from models import Case, User

def require_case_access():
    """Dependency factory: Ensures the user has jurisdiction/access to the specific case_id."""
    def checker(case_id: str, user: TokenData = Depends(get_current_user)):
        db = SessionLocal()
        try:
            case = db.query(Case).filter(Case.id == case_id).first()
            if not case:
                raise HTTPException(status_code=404, detail="Case not found")
            
            db_user = db.query(User).filter(User.username == user.username).first()
            
            # Admins bypass jurisdiction checks
            if ROLE_LEVELS.get(user.role, 0) >= ROLE_LEVELS.get("admin", 4):
                return user
                
            # If jurisdiction is set on both, they must match
            if case.jurisdiction and db_user and db_user.jurisdiction:
                if case.jurisdiction != db_user.jurisdiction:
                    raise HTTPException(status_code=403, detail="Access denied: Out of jurisdiction.")
                    
            return user
        finally:
            db.close()
    return checker


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not pwd_context.verify(form_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        token = create_access_token({"sub": user.username, "role": user.role.value})
        return {"access_token": token, "token_type": "bearer", "role": user.role.value}
    finally:
        db.close()

