import asyncio
from backend.database import engine, Base
from backend.models import BreachedHash

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")

asyncio.run(create_tables())