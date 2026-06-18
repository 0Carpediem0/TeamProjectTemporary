"""
Правило проверки длины пароля.
Возвращает количество баллов за длину и, возможно, причину.
"""

from ..config import (
    LENGTH_SCORE_8_11,
    LENGTH_SCORE_12_15,
    LENGTH_SCORE_16_PLUS,
    MAX_LENGTH,
    MIN_LENGTH,
)


def evaluate_length(password: str) -> tuple[int, str | None]:
    length = len(password)

    if length < MIN_LENGTH:
        return 0, f"Увеличьте длину пароля хотя бы до {MIN_LENGTH} символов"

    if length <= 11:
        return LENGTH_SCORE_8_11, "Для лучшей защиты используйте 12+ символов"

    if length <= 15:
        return LENGTH_SCORE_12_15, "Для максимальной защиты используйте 16+ символов"

    if length <= MAX_LENGTH:
        return LENGTH_SCORE_16_PLUS, None

    return 0, f"Уменьшите длину пароля до {MAX_LENGTH} символов"
