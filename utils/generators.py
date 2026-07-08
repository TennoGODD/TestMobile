# generators.py
"""Генерация кодов для сканирования, которых нет в БД заранее."""

import random
import string
from datetime import datetime


def generate_kitu_code(gtin: str, line: int) -> str:
    """Код КИТУ (агрегат уровня 1).

    КИТУ не существует в БД до сканирования — он появляется там только после
    того, как его отсканировали, поэтому код генерируем сами.

    Формат: 01 + GTIN (14 цифр) + линия (3 цифры) + ддммгг + 8 случайных
    букв/цифр. Пример: 0107665585002196068080726KjccKAtW.
    """
    date_part = datetime.now().strftime("%d%m%y")
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"01{gtin}{int(line):03d}{date_part}{random_part}"
