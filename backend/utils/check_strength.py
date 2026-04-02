import re

from sqlalchemy.ext.asyncio import AsyncSession

from backend.utils.check_breached_password import check_breached_password


async def check_strength(db: AsyncSession, password: str) -> dict[str, str | int | list[str]]:
    scores: int = 0
    reasons: list[str] = []
    final_strength: str = 'weak'
    breach_found = await check_breached_password(db, password)

    if len(password) < 8:
        reasons.append('Слишком короткий (менее 8 символов)')
        return {
            'strength': final_strength,
            'scores': scores,
            'reasons': reasons
        }

    if breach_found:
        reasons.append('Обнаружен в базе утечек')
        return {
            'strength': final_strength,
            'scores': scores,
            'reasons': reasons
        }

    if 8 <= len(password) <= 11:
        scores += 1

    elif len(password) >= 12:
        scores += 2

    has_digit = bool(re.search(r'\d', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_special = bool(re.search(r'[!@#$%^]', password))

    if has_digit:
        scores += 1
    else:
        scores = max(scores - 1, 0)
        reasons.append('Не содержит цифр')

    if has_upper:
        scores += 1
    else:
        scores = max(scores - 1, 0)
        reasons.append('Не содержит заглавных букв')

    if has_special:
        scores += 1
    else:
        scores = max(scores - 1, 0)
        reasons.append('Не содержит специальных символов (!@#$%^)')

    if password.isdigit():
        scores = max(scores - 1, 0)
        reasons.append('Содержит только цифры')
    elif password.isalpha() and password.islower():
        scores = max(scores - 1, 0)
        reasons.append('Содержит только строчные буквы')

    forbidden_count = 0

    if re.search(r'123|1234|12345', password):
        forbidden_count += 1
        reasons.append('Содержит простую числовую последовательность (123, 1234 и т.д.)')

    if re.search(r'qwerty|qwerty123|asdfgh|zxcvbn', password, re.IGNORECASE):
        forbidden_count += 1
        reasons.append('Содержит клавиатурную последовательность (qwerty)')

    if re.search(r'password|admin', password, re.IGNORECASE):
        forbidden_count += 1
        reasons.append('Содержит популярный пароль (password, admin)')

    if re.search(r'(.)\1{3,}', password):
        forbidden_count += 1
        reasons.append('Содержит повторяющиеся символы')

    if re.search(r'\b(19|20)\d{2}\b', password):
        forbidden_count += 1
        reasons.append('Содержит год или дату')

    if forbidden_count >= 2:
        scores = max(scores - 2, 0)
    elif forbidden_count == 1:
        scores = max(scores - 1, 0)

    if scores <= 1:
        final_strength = 'weak'
    elif scores <= 3:
        final_strength = 'medium'
    else:
        final_strength = 'strong'

    return {
        'strength': final_strength,
        'scores': scores,
        'reasons': reasons
    }
