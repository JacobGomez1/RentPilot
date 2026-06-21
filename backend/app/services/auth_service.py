from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, email: str, password: str):

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return {
        "user": user,
        "token": token
    }


def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({"sub": str(user.id)})

    return {
        "user": user,
        "token": token
    }