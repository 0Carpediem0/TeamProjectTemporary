"""
Скрипт для заполнения таблицы breached_hashes синтетическими данными.
"""

import argparse
import asyncio
import random
import string
import sys
from pathlib import Path
from typing import List, Set

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# from backend.database import async_session
# from backend.utils.hash import hash_password


# -------------------------------------------------------------------
# Генерация паролей
# -------------------------------------------------------------------
def generate_popular_passwords() -> List[str]:
    return [
        # Классика
        "123456",
        "123456789",
        "12345678",
        "12345",
        "123123",
        "111111",
        "000000",
        "654321",
        "qwerty",
        "qwerty123",
        "qwertyuiop",
        "asdfgh",
        "zxcvbn",
        "abc123",
        "password",
        "password1",
        "password123",
        "passw0rd",
        "welcome",
        "letmein",
        "master",
        "hello",
        "freedom",
        "whatever",
        "sunshine",
        "princess",
        "monkey",
        # Администрирование и IT
        "admin",
        "admin123",
        "administrator",
        "root",
        "root123",
        "postgres",
        "postgres123",
        "postgresql",
        "mysql",
        "mysql123",
        "redis",
        "redis123",
        "docker",
        "docker123",
        "nginx",
        "nginx123",
        "ubuntu",
        "ubuntu123",
        # Игры
        "minecraft",
        "minecraft123",
        "roblox",
        "roblox123",
        "fortnite",
        "fortnite123",
        "valorant",
        "valorant123",
        "cs2",
        "cs2123",
        "dota2",
        "dota2123",
        "leagueoflegends",
        # Соцсети и сервисы
        "telegram",
        "telegram123",
        "youtube",
        "youtube123",
        "instagram",
        "instagram123",
        "tiktok",
        "tiktok123",
        "discord",
        "discord123",
        "spotify",
        "spotify123",
        "google",
        "google123",
        "netflix",
        "netflix123",
        # Имена
        "alex",
        "alex123",
        "ivan",
        "ivan123",
        "anna",
        "anna123",
        "maria",
        "maria123",
        "maksim",
        "maksim123",
        # Сезоны
        "Summer",
        "Winter",
        "Spring",
        "Autumn",
    ]


# Генерация случайного пароля заданной длины.
def generate_random_password(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))


# Генерация набора уникальных случайных паролей.
def generate_random_passwords(count: int) -> List[str]:
    passwords = set()
    while len(passwords) < count:
        length = random.randint(6, 16)
        passwords.add(generate_random_password(length))
    return list(passwords)


# Генерация вариаций популярного пароля.
def generate_common_variants(base: str) -> List[str]:
    variants = set()
    years = ["2023", "2024", "2025", "2026"]
    symbols = ["!", "@", "#", "$"]

    for year in years:
        variants.add(f"{base}{year}")

    for digit in range(10):
        variants.add(f"{base}{digit}")

    for symbol in symbols:
        variants.add(f"{base}{symbol}")

    variants.add(base.capitalize())
    variants.add(base.upper())

    return list(variants)


# Добавляем генерацию дат
def generate_date_passwords() -> List[str]:
    passwords = []

    for year in range(1980, 2011):
        passwords.append(f"0101{year}")
        passwords.append(f"3112{year}")
        passwords.append(f"1505{year}")

    return passwords


# Добавляем генерацию телефонных шаблонов
def generate_phone_passwords(count: int = 2000) -> List[str]:
    passwords = []

    for _ in range(count):
        passwords.append(f"79{random.randint(100000000, 999999999)}")

    return passwords


# Генерация общего набора паролей.
def generate_all_passwords(total_count: int, popular_ratio: float = 0.3) -> List[str]:
    popular_count = int(total_count * popular_ratio)
    random_count = total_count - popular_count
    popular_passwords = set()
    popular_list = generate_popular_passwords()
    popular_passwords.update(popular_list)

    for base in popular_list:
        popular_passwords.update(generate_common_variants(base))

    popular_passwords.update(generate_date_passwords())
    popular_passwords.update(generate_phone_passwords())

    while len(popular_passwords) < popular_count:
        popular_passwords.update(
            generate_random_passwords(min(1000, popular_count - len(popular_passwords)))
        )

    random_passwords = generate_random_passwords(random_count)
    all_passwords = list(popular_passwords) + random_passwords
    random.shuffle(all_passwords)

    return all_passwords[:total_count]


# -------------------------------------------------------------------
# Вставка в БД
# -------------------------------------------------------------------
async def insert_hashes_batch(
    session: AsyncSession, hashes: Set[str], batch_size: int = 1000
):  # Пакетная вставка хэшей в базу.
    hashes_list = list(hashes)  # Преобразование множества в список.
    for i in range(0, len(hashes_list), batch_size):  # Разбиение данных на пакеты.
        batch = hashes_list[i : i + batch_size]  # Выделение текущего пакета.
        # Для SQLite используем INSERT OR IGNORE
        stmt = text("""
            INSERT OR IGNORE INTO breached_hashes (hash_password)
            VALUES (:hash_value)
        """)
        await session.execute(
            stmt, [{"hash_value": h} for h in batch]
        )  # Выполнение вставки пакета.
        await session.commit()
        print(
            f"Вставлено {min(i + batch_size, len(hashes_list))} из {len(hashes_list)} записей..."
        )


async def populate(total_count: int = 100000, popular_ratio: float = 0.3):
    """Основная функция заполнения."""
    async with async_session() as session:
        print(f"Генерация {total_count} паролей...")
        passwords = generate_all_passwords(
            total_count, popular_ratio
        )  # Генерация паролей.
        print(f"Сгенерировано {len(passwords)} паролей.")

        print("Вычисление SHA-256 хэшей...")
        hashes = {hash_password(pwd) for pwd in passwords}  # Хеширование паролей.
        print(f"Уникальных хэшей: {len(hashes)}")

        print("Вставка в базу данных...")
        await insert_hashes_batch(session, hashes)  # Вызов пакетной вставки.

    print("Готово!")


# -------------------------------------------------------------------
# Точка входа
# -------------------------------------------------------------------
def main():  # Основная точка входа в программу.
    parser = argparse.ArgumentParser(
        description="Заполнение таблицы breached_hashes"
    )  # Создание парсера аргументов.
    parser.add_argument(
        "--count",
        type=int,
        default=100000,
        help="Количество паролей для генерации (по умолчанию 100000)",
    )  # Аргумент количества паролей.
    parser.add_argument(
        "--popular-ratio",
        type=float,
        default=0.3,
        help="Доля популярных паролей (0..1, по умолчанию 0.3)",
    )  # Аргумент доли популярных паролей.
    args = parser.parse_args()  # Разбор аргументов командной строки.

    asyncio.run(
        populate(args.count, args.popular_ratio)
    )  # Запуск асинхронной функции заполнения.


if __name__ == "__main__":
    main()
