from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Определение строки подключения к SQLite-базе данных.
DATABASE_URL = "sqlite+aiosqlite:///./backend/data/breached_hashes.db"

 # Создание асинхронного движка для взаимодействия с базой данных.
engine = create_async_engine(DATABASE_URL, echo=True)

 # Создание фабрики асинхронных сессий.
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

 # Создание базового класса для всех моделей базы данных.
class Base(DeclarativeBase): pass
