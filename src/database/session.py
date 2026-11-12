from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

<<<<<<< HEAD
# Путь к нашей базе данных SQLite (из ЛР №5)
SQLALCHEMY_DATABASE_URL = "sqlite:///./docs/sql/request.db"

# Создаем движок. check_same_thread=False нужен для SQLite при работе с FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаем фабрику сессий (через нее мы будем делать запросы к БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для наших моделей
=======
SQLALCHEMY_DATABASE_URL = "sqlite:///./docs/sql/request.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> feature/lab6
Base = declarative_base()