from sqlalchemy.orm import Session
from src.models.orm import Request
from src.models.schemas import RequestCreate
from datetime import datetime

class RequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, request_data: RequestCreate, number: str) -> Request:
        """Создает новую заявку в БД"""
        db_request = Request(
            number=number,
            title=request_data.title,
            description=request_data.description,
            priority=request_data.priority,
            author_id=request_data.author_id,
            category_id=request_data.category_id,
            status_id=1, # По умолчанию статус "Новая" (ID=1 из seed.sql)
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request) # Обновляем объект, чтобы получить ID из БД
        return db_request

    def get_all(self, skip: int = 0, limit: int = 100):
        """Возвращает список заявок с пагинацией"""
        return self.db.query(Request).offset(skip).limit(limit).all()

    def get_by_id(self, request_id: int) -> Request:
        """Возвращает одну заявку по ID"""
        return self.db.query(Request).filter(Request.id == request_id).first()

    def get_last_number(self) -> str:
        """Находит номер последней созданной заявки для генерации нового"""
        last_request = self.db.query(Request).order_by(Request.id.desc()).first()
        return last_request.number if last_request else None

    def update(self, request_id: int, update_data: dict):
        """Обновляет поля заявки"""
        db_request = self.get_by_id(request_id)
        if db_request:
            for key, value in update_data.items():
                setattr(db_request, key, value)
            self.db.commit()
            self.db.refresh(db_request)
        return db_request

    def delete(self, request_id: int):
        """Удаляет заявку (или архивирует, если по ТЗ запрещено удалять)"""
        db_request = self.get_by_id(request_id)
        if db_request:
            # По ТЗ мы не удаляем, а архивируем (переводим в статус 4 "Закрыта")
            db_request.status_id = 4 
            self.db.commit()
        return db_request
        
    def search_and_filter(self, status_id: int = None, category_id: int = None, priority: str = None, search_query: str = None):
        """Поиск и фильтрация заявок"""
        query = self.db.query(Request)
        
        if status_id:
            query = query.filter(Request.status_id == status_id)
        if category_id:
            query = query.filter(Request.category_id == category_id)
        if priority:
            query = query.filter(Request.priority == priority)
        if search_query:
            # Поиск по номеру или названию
            search_pattern = f"%{search_query}%"
            query = query.filter((Request.number.like(search_pattern)) | (Request.title.like(search_pattern)))
            
        return query.all()