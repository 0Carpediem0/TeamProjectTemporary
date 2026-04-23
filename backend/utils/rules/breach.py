from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.passwords import BreachedHash
from backend.utils.hash import hash_password


async def check_breached_password(db: AsyncSession, password: str) -> bool:
    hashed_password = hash_password(password)
    breached_password = (await db.scalars(
        select(BreachedHash).where(BreachedHash.hash_password == hashed_password)
    )).first()
    if breached_password is not None:
        return True
    return False
