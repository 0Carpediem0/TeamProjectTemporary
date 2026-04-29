"""
Правила обнаружения запрещённых шаблонов:
числовые и клавиатурные последовательности, популярные слова, повторы, годы.
"""

from ..config import FORBIDDEN_PATTERNS, PENALTY_FORBIDDEN_ONE, PENALTY_FORBIDDEN_TWO_PLUS


def evaluate_forbidden_patterns(password: str) -> tuple[int, list[str]]:
    """
    Ищет запрещённые паттерны в пароле.
    """
    reasons_map = {
        'numeric_sequence': 'Избегайте последовательностей цифр (123, 1234)',
        'keyboard': 'Не используйте соседние клавиши на клавиатуре (qwerty, asdfgh)',
        'repeat': 'Избегайте повторения одного символа подряд (aaaa, 1111)',
        'year': 'Не используйте годы или даты в пароле',
    }

    found_reasons = []
    for pattern_key, pattern_regex in FORBIDDEN_PATTERNS.items():
        if pattern_regex.search(password):
            found_reasons.append(reasons_map[pattern_key])

    if len(found_reasons) >= 2:
        penalty = PENALTY_FORBIDDEN_TWO_PLUS
    elif len(found_reasons) == 1:
        penalty = PENALTY_FORBIDDEN_ONE
    else:
        penalty = 0

    return penalty, found_reasons
