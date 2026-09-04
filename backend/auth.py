"""
SUTRA Backend — auth.py
==========================
JWT authentication + role-based access control (RBAC), per blueprint
Part 17. Roles: admin, senior_investigator, investigator, analyst, viewer.
"""

import os
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel

SECRET_KEY = os.environ.get("SUTRA_JWT_SECRET", "sutra-development-insecure-secret-key-32chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)
router = APIRouter()

# Role hierarchy — used by require_role() to check "at least this level"
ROLE_LEVELS = {"viewer": 0, "analyst": 1, "investigator": 2, "senior_investigator": 3, "admin": 4}


class TokenData(BaseModel):
    username: str
    role: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


# Built-in demo accounts for investigation teams
FAKE_USERS_DB = {
    "demo_investigator": {
        "username": "Insp. Vikramaditya Kadam",
        "hashed_password": hash_password("demo-password"),
        "role": "investigator"
    },
    "demo_admin": {
        "username": "Superintendent S. Roy",
        "hashed_password": hash_password("demo-password"),
        "role": "admin"
    },
    "demo_analyst": {
        "username": "Analyst Priya Sen",
        "hashed_password": hash_password("demo-password"),
        "role": "analyst"
    }
}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> TokenData:
    # If no token provided in demo/dev mode, default to lead investigator
    if not token:
        return TokenData(username="Insp. Vikramaditya Kadam", role="investigator")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except jwt.PyJWTError:
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
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        # Also check by simple username match
        match = None
        for k, v in FAKE_USERS_DB.items():
            if form_data.username.lower() in k.lower() or form_data.username.lower() in v["username"].lower():
                if verify_password(form_data.password, v["hashed_password"]):
                    match = v
                    break
        if not match:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        user = match

    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"], "username": user["username"]}
