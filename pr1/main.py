"""ПР1: стартовый сценарий планировщика приготовления блюд."""
from datetime import datetime, timedelta

dish_name = "Запеченная курица с картофелем"
prep_minutes = int("20")   # активная подготовка (преобразование типов)
cook_minutes = int("75")   # запекание в духовке
serve_time = datetime(2026, 9, 20, 19, 0)
now = datetime(2026, 9, 20, 16, 30)


def calculate_total_time(prep, cook):
    """Вернуть общее время приготовления блюда в минутах."""
    return prep + cook


def calculate_start_time(serve_at, total_minutes):
    """Вернуть время, когда нужно начать готовить блюдо."""
    return serve_at - timedelta(minutes=total_minutes)


def format_duration(minutes):
    """Преобразовать минуты в строку вида '1 ч 35 мин'."""
    hours = minutes // 60
    mins = minutes % 60
    if hours == 0:
        return f"{mins} мин"
    if mins == 0:
        return f"{hours} ч"
    return f"{hours} ч {mins} мин"


def get_start_status(start_time, current_time):
    """Вернуть текстовый статус: успеваем ли мы к подаче."""
    if start_time < current_time:
        return "Опаздываем: начинать нужно было раньше"
    if start_time == current_time:
        return "Пора начинать прямо сейчас"
    return "Времени достаточно, можно подождать"


total_minutes = calculate_total_time(prep_minutes, cook_minutes)
start_time = calculate_start_time(serve_time, total_minutes)

print(f"Блюдо: {dish_name}")
print(f"Общее время: {format_duration(total_minutes)}")
print(f"Подача: {serve_time:%d.%m.%Y %H:%M}")
print(f"Начать готовить в: {start_time:%H:%M}")
print(get_start_status(start_time, now))
