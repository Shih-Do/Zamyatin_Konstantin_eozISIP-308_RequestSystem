from sqlalchemy.orm import Session
from src.repositories.request_repository import RequestRepository
from src.models.schemas import RequestCreate
from datetime import datetime

class RequestService:
    def __init__(self, db: Session):
        self.repository = RequestRepository(db)
    def _generate_request_number(self) -> str:
        current_year = datetime.now().year
        last_number = self.repository.get_last_number()
        if not last_number:
            return f"#{current_year}-0001"
        try:
            last_seq = int(last_number.split('-')[1])
            return f"#{current_year}-{last_seq + 1:04d}"
        except (IndexError, ValueError):
            return f"#{current_year}-0001"
    def create_request(self, request_data: RequestCreate):
        return self.repository.create(request_data, self._generate_request_number())
    def get_requests(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)
    def get_request(self, request_id: int):
        return self.repository.get_by_id(request_id)
    def update_request(self, request_id: int, update_data: dict):
        return self.repository.update(request_id, update_data)
    def archive_request(self, request_id: int):
        return self.repository.delete(request_id)
    def search_requests(self, status_id: int = None, category_id: int = None, priority: str = None, search_query: str = None):
        return self.repository.search_and_filter(status_id, category_id, priority, search_query)