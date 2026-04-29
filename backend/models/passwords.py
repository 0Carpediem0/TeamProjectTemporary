from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


class BreachedHash(Base):
    __tablename__ = 'breached_hashes'

    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    hash_password: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
