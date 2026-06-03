from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Создание зависимости для получения сессии базы данных.
    """
    async_session = request.app.state.async_session
    async with async_session() as session:
        yield session
