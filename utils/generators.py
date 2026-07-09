# generators.py

import random
import string
from datetime import datetime


def generate_kitu_code(gtin: str, line: int) -> str:

    date_part = datetime.now().strftime("%d%m%y")
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"01{gtin}{int(line):03d}{date_part}{random_part}"
