"""
Правило проверки длины пароля.
Возвращает количество баллов за длину и, возможно, причину.
"""

from ..config import MIN_LENGTH, LENGTH_SCORE_8_11, LENGTH_SCORE_12_PLUS, MAX_LENGTH


def evaluate_length(password: str) -> tuple[int, str | None]:
    """
    Вычисляет балл за длину пароля.
    """
    length = len(password)
    if length < MIN_LENGTH:
        return 0, f'Увеличьте длину пароля хотя бы до {MIN_LENGTH} символов'
    elif MIN_LENGTH <= length <= 11:
        return LENGTH_SCORE_8_11, f'Увеличьте длину пароля до 12 символов'
    else:
        return LENGTH_SCORE_12_PLUS, None
