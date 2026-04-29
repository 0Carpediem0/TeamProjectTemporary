"""
Правила состава пароля: наличие цифр, заглавных букв, спецсимволов,
а также штрафы за пароли только из цифр или только из букв.
"""

import re
from ..config import (
    BONUS_HAS_DIGIT, BONUS_HAS_UPPER, BONUS_HAS_SPECIAL,
    PENALTY_ONLY_DIGITS, PENALTY_ONLY_LETTERS, PENALTY_ONLY_LOWERCASE,
)


def evaluate_composition(password: str) -> tuple[int, list[str]]:
    """
    Анализирует символьный состав пароля.
    """
    score = 0
    reasons = []

    has_digit = bool(re.search(r'\d', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_special = bool(re.search(r'[!@#$%^_]', password))

    if has_digit:
        score += BONUS_HAS_DIGIT
    else:
        score += PENALTY_ONLY_LETTERS
        reasons.append('Добавьте хотя бы одну цифру')
    if has_upper:
        score += BONUS_HAS_UPPER
    else:
        score += PENALTY_ONLY_LOWERCASE
        reasons.append('Используйте заглавные буквы')
    if has_special:
        score += BONUS_HAS_SPECIAL
    else:
        reasons.append('Добавьте специальные символы (! @ # $ % ^)')

    if password.isdigit():
        score += PENALTY_ONLY_DIGITS
        reasons.append('Добавьте буквы (заглавные и строчные) и специальные символы')

    return score, reasons
