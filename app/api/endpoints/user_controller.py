from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_user import authenticate_user, create_user, get_user_by_email
from app.db.session import SessionLocal
from app.schemas.schema_token import Token
from app.schemas.schema_user import UserCreate, UserResponse, UserRole
from app.utils.dependencies import require_role
from app.utils.security import create_access_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/admin-data", dependencies=[require_role(UserRole.admin)])
def read_admin_data():
    return {"message": "This data is only for admins"}


@router.get("/user-data", dependencies=[require_role(UserRole.user)])
def read_user_data():
    return {"message": "This data is for users"}


@router.post("/create", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role.value,
    }
