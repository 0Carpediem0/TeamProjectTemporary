from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Определение строки подключения к SQLite-базе данных.
DATABASE_URL = "sqlite+aiosqlite:///./backend/data/breached_hashes.db"
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = async_sessionmaker(
# bind=engine, expire_on_commit=True, class_=AsyncSession
# )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание асинхронного движка для взаимодействия с базой данных.
    engine = create_async_engine(DATABASE_URL, echo=True)
    # Создание фабрики асинхронных сессий.
    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=True, class_=AsyncSession
    )
    app.state.async_session = async_session
    yield
    await engine.dispose()


# Создание базового класса для всех моделей базы данных.
class Base(DeclarativeBase):
    pass
