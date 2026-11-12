from sqlalchemy.orm import Session
from src.models.orm import Request
from src.models.schemas import RequestCreate
from datetime import datetime

class RequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, request_data: RequestCreate, number: str) -> Request:
        db_request = Request(
            number=number,
            title=request_data.title,
            description=request_data.description,
            priority=request_data.priority,
            author_id=request_data.author_id,
            category_id=request_data.category_id,
            status_id=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        return db_request

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Request).offset(skip).limit(limit).all()

    def get_by_id(self, request_id: int) -> Request:
        return self.db.query(Request).filter(Request.id == request_id).first()

    def get_last_number(self) -> str:
        last_request = self.db.query(Request).order_by(Request.id.desc()).first()
        return last_request.number if last_request else None

    def update(self, request_id: int, update_data: dict):
        db_request = self.get_by_id(request_id)
        if db_request:
            for key, value in update_data.items():
                setattr(db_request, key, value)
            self.db.commit()
            self.db.refresh(db_request)
        return db_request

    def delete(self, request_id: int):
        db_request = self.get_by_id(request_id)
        if db_request:
            db_request.status_id = 4 
            self.db.commit()
        return db_request
        
    def search_and_filter(self, status_id: int = None, category_id: int = None, priority: str = None, search_query: str = None):
        query = self.db.query(Request)
        
        if status_id:
            query = query.filter(Request.status_id == status_id)
        if category_id:
            query = query.filter(Request.category_id == category_id)
        if priority:
            query = query.filter(Request.priority == priority)
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter((Request.number.like(search_pattern)) | (Request.title.like(search_pattern)))
            
        return query.all()