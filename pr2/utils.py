"""Вспомогательные функции: безопасный ввод и форматирование."""
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
            print("Ошибка: формат ДД.ММ.ГГГГ ЧЧ:ММ, например 20.09.2026 19:00")


def format_duration(minutes: int) -> str:
    """Преобразовать минуты в строку вида '1 ч 35 мин'."""
    hours, mins = divmod(minutes, 60)
    if hours == 0:
        return f"{mins} мин"
    if mins == 0:
        return f"{hours} ч"
    return f"{hours} ч {mins} мин"
