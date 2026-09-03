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

SECRET_KEY = os.environ.get("SUTRA_JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

# Role hierarchy — used by require_role() to check "at least this level"
ROLE_LEVELS = {"viewer": 0, "analyst": 1, "investigator": 2, "senior_investigator": 3, "admin": 4}


class TokenData(BaseModel):
    username: str
    role: str


# NOTE: replace with a real users table lookup (SQLAlchemy) in production.
FAKE_USERS_DB = {
    "demo_investigator": {"username": "demo_investigator", "hashed_password": pwd_context.hash("demo-password"), "role": "investigator"},
    "demo_admin": {"username": "demo_admin", "hashed_password": pwd_context.hash("demo-password"), "role": "admin"},
}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception


def require_role(min_role: str):
    """Dependency factory: require_role('investigator') blocks viewers/analysts."""
    def checker(user: TokenData = Depends(get_current_user)):
        if ROLE_LEVELS.get(user.role, -1) < ROLE_LEVELS.get(min_role, 99):
            raise HTTPException(status_code=403, detail=f"Requires role '{min_role}' or higher")
        return user
    return checker


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = FAKE_USERS_DB.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}
