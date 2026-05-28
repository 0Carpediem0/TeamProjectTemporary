"""
Правило проверки длины пароля.
Возвращает количество баллов за длину и, возможно, причину.
"""

from ..config import LENGTH_SCORE_8_11, LENGTH_SCORE_12_PLUS, MAX_LENGTH, MIN_LENGTH


def evaluate_length(password: str) -> tuple[int, str | None]:
    """
    Вычисляет балл за длину пароля.
    """
    length = len(password)
    if length < MIN_LENGTH:
        return 0, f"Увеличьте длину пароля хотя бы до {MIN_LENGTH} символов"
    elif MIN_LENGTH <= length <= 11:
        return LENGTH_SCORE_8_11, "Увеличьте длину пароля до 12 символов"
    elif 12 <= length <= MAX_LENGTH:
        return LENGTH_SCORE_12_PLUS, None
    else:
        return 0, f"Уменьшите длину пароля до {MAX_LENGTH} символов"
