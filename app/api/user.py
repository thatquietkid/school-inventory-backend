# app/api/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse
from app.models.user import User
from app.db.database import get_db
from app.auth.dependencies import require_role

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db),
               user=Depends(require_role(["Administrator"]))):
    return db.query(User).all()

