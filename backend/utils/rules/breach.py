"""
Модуль для проверки пароля по базе утечек.
В учебном проекте обращается к базе данных через сессию SQLAlchemy.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.passwords import BreachedHash
from backend.utils.hash import hash_password


async def is_password_breached(db: AsyncSession, password: str) -> bool:
    """
    Проверяет, найден ли пароль в базе утечек (по SHA-256 хэшу).
    """
    hashed_password = hash_password(password)
    breached_password = (await db.scalars(
        select(BreachedHash).where(BreachedHash.hash_password == hashed_password)
    )).first()
    return breached_password is not None
