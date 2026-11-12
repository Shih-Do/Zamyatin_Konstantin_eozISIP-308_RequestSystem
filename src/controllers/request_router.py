from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.session import SessionLocal
from src.services.request_service import RequestService
from src.models.schemas import RequestCreate, RequestResponse

# Создаем роутер для группировки эндпоинтов
router = APIRouter(prefix="/api/v1/requests", tags=["Заявки"])

# Функция для получения сессии БД в рамках одного запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[RequestResponse])
def get_requests(
    skip: int = 0, 
    limit: int = 100, 
    status_id: int = None, 
    category_id: int = None, 
    priority: str = None, 
    q: str = None, # q - это параметр для поиска по тексту
    db: Session = Depends(get_db)
):
    """Получение списка заявок с поиском и фильтрацией"""
    service = RequestService(db)
    return service.search_requests(status_id=status_id, category_id=category_id, priority=priority, search_query=q)

@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(request_data: RequestCreate, db: Session = Depends(get_db)):
    """Создание новой заявки"""
    service = RequestService(db)
    return service.create_request(request_data)

@router.get("/{request_id}", response_model=RequestResponse)
def get_request(request_id: int, db: Session = Depends(get_db)):
    """Получение заявки по ID"""
    service = RequestService(db)
    request = service.get_request(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return request

@router.patch("/{request_id}", response_model=RequestResponse)
def update_request(request_id: int, update_data: dict, db: Session = Depends(get_db)):
    """Обновление заявки (изменение полей, статуса, назначение исполнителя)"""
    service = RequestService(db)
    request = service.get_request(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return service.update_request(request_id, update_data)

@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    """Архивация заявки (перевод в статус Закрыта)"""
    service = RequestService(db)
    request = service.get_request(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    service.archive_request(request_id)
    return None