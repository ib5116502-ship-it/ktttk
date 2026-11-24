from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings


# Подключение к PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)


# Создание сессий
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Базовый класс моделей
class Base(DeclarativeBase):
    pass


# Получение сессии базы данных
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()