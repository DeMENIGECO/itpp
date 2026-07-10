from __future__ import annotations

import random
from typing import Any


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def as_number(value: Any) -> float:
    if isinstance(value, bool):
        raise TypeError("Il valore booleano non può essere convertito in numero.")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError as exc:
            raise TypeError("Il valore non è un numero valido.") from exc
    raise TypeError("Il valore non è numerico.")


def to_string(value: Any) -> str:
    if value is None:
        return "nullo"
    if isinstance(value, bool):
        return "vero" if value else "falso"
    if isinstance(value, list):
        return "[" + ", ".join(to_string(v) for v in value) + "]"
    if isinstance(value, dict):
        items = ", ".join(f"{k}: {to_string(v)}" for k, v in value.items())
        return "{" + items + "}"
    return str(value)


def random_int(a: int, b: int) -> int:
    return random.randint(a, b)
