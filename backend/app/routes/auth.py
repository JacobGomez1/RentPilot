from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, authenticate_user
from app.core.security import decode_token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# REGISTER
# -------------------------
@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):

    result = register_user(db, payload.email, payload.password)

    if not result:
        raise HTTPException(status_code=400, detail="Email already exists")

    return {
        "access_token": result["token"],
        "token_type": "bearer"
    }


# -------------------------
# LOGIN
# -------------------------
@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    result = authenticate_user(db, payload.email, payload.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": result["token"],
        "token_type": "bearer"
    }


# -------------------------
# PROTECTED ROUTE (NEW)
# -------------------------
@router.get("/me", response_model=UserResponse)
def get_me(token: str, db: Session = Depends(get_db)):

    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user