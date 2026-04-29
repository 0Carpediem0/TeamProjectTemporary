"""
Главная функция проверки стойкости пароля.
Оркестрирует вызовы отдельных правил, обрабатывает автоматически слабые случаи,
подсчитывает итоговый балл и формирует ответ.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from .config import WEAK_THRESHOLD, MEDIUM_THRESHOLD
from .rules.breach import is_password_breached
from .rules.length import evaluate_length
from .rules.composition import evaluate_composition
from .rules.forbidden import evaluate_forbidden_patterns


async def check_strength(db: AsyncSession, password: str) -> dict[str, str | int | list[str]]:
    """
        Асинхронно оценивает стойкость пароля по заданным правилам.

        Returns:
            dict со структурой:
            {
                'strength': 'weak' | 'medium' | 'strong',
                'scores': int,
                'reasons': list[str]
            }
    """
    stripped = password.strip()
    total_score = 0
    all_reasons = []

    if not stripped:
        return {
            'strength': 'weak',
            'scores': 0,
            'reasons': ['Введите пароль']
        }

    if await is_password_breached(db, stripped):
        return {
            'strength': 'weak',
            'scores': total_score,
            'reasons': ['Обнаружен в базе утечек']
        }

    length_score, length_reason = evaluate_length(stripped)
    if length_score == 0:
        return {
            'strength': 'weak',
            'scores': total_score,
            'reasons': [length_reason]
        }
    total_score += length_score
    if length_reason:
        all_reasons.append(length_reason)

    comp_score, comp_reasons = evaluate_composition(stripped)
    total_score += comp_score
    all_reasons.extend(comp_reasons)

    forb_score, forb_reasons = evaluate_forbidden_patterns(stripped)
    total_score += forb_score
    all_reasons.extend(forb_reasons)

    total_score = max(total_score, 0)

    if total_score <= WEAK_THRESHOLD:
        strength = 'weak'
    elif total_score <= MEDIUM_THRESHOLD:
        strength = 'medium'
    else:
        strength = 'strong'

    return {
        'strength': strength,
        'scores': total_score,
        'reasons': all_reasons
    }
