"""
Конфигурация правил проверки пароля.
Все весовые коэффициенты, пороги и регулярные выражения.
"""

import re

# ----- Пороги длины и баллы ------------------------------------------------
MIN_LENGTH = 8
MAX_LENGTH = 128
LENGTH_SCORE_8_11 = 1
LENGTH_SCORE_12_PLUS = 2

# ----- Штрафы и бонусы состава ---------------------------------------------
BONUS_HAS_DIGIT = 1
BONUS_HAS_UPPER = 1
BONUS_HAS_SPECIAL = 1

PENALTY_ONLY_DIGITS = -1
PENALTY_ONLY_LETTERS = -1
PENALTY_ONLY_LOWERCASE = -1

# ----- Штрафы за запрещённые паттерны ---------------------------------------
PENALTY_FORBIDDEN_ONE = -1
PENALTY_FORBIDDEN_TWO_PLUS = -2

# ----- Итоговые пороги оценки -----------------------------------------------
WEAK_THRESHOLD = 1
MEDIUM_THRESHOLD = 3

# ----- Регулярные выражения для поиска паттернов ----------------------------
FORBIDDEN_PATTERNS = {
    'numeric_sequence': re.compile(r'123|1234|12345'),
    'keyboard': re.compile(r'qwerty|asdfgh|zxcvbn', re.IGNORECASE),
    'repeat': re.compile(r'(.)\1{2,}'),
    'year': re.compile(r'(?<!\d)(?:19|20)\d{2}(?!\d)|\d{1,2}[./-]\d{1,2}[./-]\d{2,4}'),
}
