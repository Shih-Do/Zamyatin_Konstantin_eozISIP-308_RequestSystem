from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.session import SessionLocal
from src.models.orm import User, Status, Category
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["Справочники"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Вспомогательные схемы для вывода (чтобы не ругался Pydantic)
class UserResponse(BaseModel):
    id: int
    name: str
    role: str

class StatusResponse(BaseModel):
    id: int
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Список всех пользователей"""
    return db.query(User).all()

@router.get("/statuses", response_model=List[StatusResponse])
def get_statuses(db: Session = Depends(get_db)):
    """Список всех статусов"""
    return db.query(Status).all()

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Список всех категорий"""
    return db.query(Category).all()