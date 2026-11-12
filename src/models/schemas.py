from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RequestCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Тема заявки")
    description: Optional[str] = Field(None, description="Подробное описание")
    priority: str = Field("Средний", description="Приоритет: Низкий, Средний, Высокий")
    category_id: int = Field(..., description="ID категории")
    author_id: int = Field(..., description="ID автора заявки")

class RequestResponse(RequestCreate):
    id: int
    number: str
    status_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True