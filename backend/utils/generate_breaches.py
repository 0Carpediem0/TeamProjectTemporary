"""
Скрипт для заполнения таблицы breached_hashes синтетическими данными.
"""

import asyncio
import random
import string
import argparse
import sys
from pathlib import Path
from typing import List, Set

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import async_session
from backend.models.passwords import BreachedHash
from backend.utils.hash import hash_password


# -------------------------------------------------------------------
# Генерация паролей
# -------------------------------------------------------------------
def generate_popular_passwords() -> List[str]:
    return [
        "123456", "password", "123456789", "12345", "12345678", "qwerty",
        "abc123", "password1", "admin", "letmein", "welcome", "monkey",
        "sunshine", "princess", "master", "hello", "freedom", "whatever",
        "qwerty123", "admin123", "iloveyou", "123123", "654321", "000000",
        "111111", "1234567", "123321", "qwertyuiop", "passw0rd"
    ]


def generate_random_password(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_passwords(count: int) -> List[str]:
    passwords = set()
    while len(passwords) < count:
        length = random.randint(6, 16)
        passwords.add(generate_random_password(length))
    return list(passwords)


def generate_common_variants(base: str, count: int = 5) -> List[str]:
    variants = []
    for i in range(1, count + 1):
        variants.append(f"{base}{i}")
        variants.append(f"{base}{random.choice('!@#$%^&*')}")
        variants.append(f"{base}{random.choice(string.digits)}")
    return variants


def generate_all_passwords(total_count: int, popular_ratio: float = 0.3) -> List[str]:
    popular_count = int(total_count * popular_ratio)
    random_count = total_count - popular_count

    # Популярные + вариации
    popular_list = generate_popular_passwords()
    popular_passwords = set(popular_list)
    for base in popular_list[:20]:
        popular_passwords.update(generate_common_variants(base, 3))
    if len(popular_passwords) < popular_count:
        popular_passwords.update(
            generate_random_passwords(popular_count - len(popular_passwords))
        )

    # Случайные
    random_passwords = generate_random_passwords(random_count)

    all_passwords = list(popular_passwords) + random_passwords
    return all_passwords[:total_count]


# -------------------------------------------------------------------
# Вставка в БД
# -------------------------------------------------------------------
async def insert_hashes_batch(session: AsyncSession, hashes: Set[str], batch_size: int = 1000):
    hashes_list = list(hashes)
    for i in range(0, len(hashes_list), batch_size):
        batch = hashes_list[i:i + batch_size]
        # Для SQLite используем INSERT OR IGNORE
        stmt = text("""
            INSERT OR IGNORE INTO breached_hashes (hash_password)
            VALUES (:hash_value)
        """)
        await session.execute(stmt, [{"hash_value": h} for h in batch])
        await session.commit()
        print(f"Вставлено {min(i + batch_size, len(hashes_list))} из {len(hashes_list)} записей...")


async def populate(total_count: int = 50000, popular_ratio: float = 0.3):
    """Основная функция заполнения."""
    async with async_session() as session:
        print(f"Генерация {total_count} паролей...")
        passwords = generate_all_passwords(total_count, popular_ratio)
        print(f"Сгенерировано {len(passwords)} паролей.")

        print("Вычисление SHA-256 хэшей...")
        hashes = {hash_password(pwd) for pwd in passwords}
        print(f"Уникальных хэшей: {len(hashes)}")

        print("Вставка в базу данных...")
        await insert_hashes_batch(session, hashes)

    print("Готово!")


# -------------------------------------------------------------------
# Точка входа
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Заполнение таблицы breached_hashes")
    parser.add_argument("--count", type=int, default=50000,
                        help="Количество паролей для генерации (по умолчанию 50000)")
    parser.add_argument("--popular-ratio", type=float, default=0.3,
                        help="Доля популярных паролей (0..1, по умолчанию 0.3)")
    args = parser.parse_args()

    asyncio.run(populate(args.count, args.popular_ratio))


if __name__ == "__main__":
    main()