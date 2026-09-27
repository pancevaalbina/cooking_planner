"""Вспомогательные функции общего назначения (не относятся к объектам)."""
from datetime import datetime


def input_int(prompt: str) -> int:
    """Запросить целое число; при ошибке повторить запрос."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_datetime(prompt: str) -> datetime:
    """Запросить дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y %H:%M")
        except ValueError:
            print("Ошибка: формат ДД.ММ.ГГГГ ЧЧ:ММ, например "
                  "20.09.2026 19:00")
