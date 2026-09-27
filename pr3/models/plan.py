"""Класс записи плана приготовления и функции работы с планом.

Модуль - аналог bookings.py из методички: PlanEntry соответствует
классу Booking, а Dish - классу Room. Вместо пользователя и даты
бронирования запись плана хранит блюдо и время подачи; вместо
"одно помещение - одна дата" здесь действует правило "у двух блюд
не могут пересекаться по времени активные (требующие повара) задачи".
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Tuple

from decorators import log_call
from models.dishes import Dish


class PlanEntry:
    """Запись плана: блюдо, время подачи и статус (активна/отменена).

    PlanEntry хранит ссылку на объект Dish (композиция), а не только
    его идентификатор - это дает прямой доступ к данным блюда:
    entry.dish.name, entry.dish.recipe.total_minutes и т.д.
    """

    def __init__(self, entry_id: int, dish: Dish,
                 serve_time: datetime) -> None:
        """Создать запись плана для блюда dish к моменту serve_time."""
        self.id = entry_id
        self.dish = dish
        self.serve_time = serve_time
        self.is_cancelled = False

    @property
    def start_time(self) -> datetime:
        """Момент, когда нужно начать готовить блюдо."""
        return self.serve_time - self.dish.total_time

    def cancel(self) -> None:
        """Отменить запись плана, не удаляя её из коллекции."""
        self.is_cancelled = True

    def active_intervals(self) -> List[Tuple[datetime, datetime]]:
        """Вернуть интервалы (начало, конец) активных задач записи."""
        intervals = []
        current = self.start_time
        for task in self.dish.recipe.tasks:
            end = current + task.duration
            if task.requires_cook:
                intervals.append((current, end))
            current = end
        return intervals

    def __str__(self) -> str:
        """Строковое представление записи с учетом её состояния."""
        state = "отменена" if self.is_cancelled else "активна"
        return (f"{self.id}. {self.dish.name}: начать в "
                f"{self.start_time:%d.%m %H:%M}, подать в "
                f"{self.serve_time:%d.%m %H:%M} ({state})")


def get_start_status(start_time: datetime, now: datetime) -> str:
    """Статус блюда относительно текущего времени (функция из ПР1)."""
    if start_time < now:
        return "Опаздываем: начинать нужно было раньше"
    if start_time == now:
        return "Пора начинать прямо сейчас"
    return "Времени достаточно, можно подождать"


def _overlaps(a: Tuple[datetime, datetime],
              b: Tuple[datetime, datetime]) -> bool:
    """Проверить, пересекаются ли два интервала времени."""
    return a[0] < b[1] and b[0] < a[1]


def is_time_free(
    entries: List[PlanEntry], dish: Dish, serve_time: datetime,
) -> bool:
    """Проверить, что новая запись не создаст конфликт по времени.

    Конфликт возникает, если активные (требующие повара) задачи новой
    записи пересекаются по времени с активными задачами уже
    существующей активной записи. Отмененные записи не учитываются.
    """
    candidate = PlanEntry(0, dish, serve_time)
    candidate_intervals = candidate.active_intervals()
    for entry in entries:
        if entry.is_cancelled:
            continue
        for existing in entry.active_intervals():
            for new_interval in candidate_intervals:
                if _overlaps(existing, new_interval):
                    return False
    return True


def _has_overlap(
    a_intervals: List[Tuple[datetime, datetime]],
    b_intervals: List[Tuple[datetime, datetime]],
) -> bool:
    """Проверить, есть ли пересечение между двумя наборами интервалов."""
    for a in a_intervals:
        for b in b_intervals:
            if _overlaps(a, b):
                return True
    return False


@log_call
def create_plan_entry(
    entries: List[PlanEntry], dishes: List[Dish],
    dish_id: int, serve_time: datetime,
) -> Optional[PlanEntry]:
    """Создать запись плана, если это не создает конфликта по времени."""
    dish = next((d for d in dishes if d.id == dish_id), None)
    if dish is None:
        raise ValueError(f"Блюдо {dish_id} не найдено")
    if not is_time_free(entries, dish, serve_time):
        return None
    entry_id = max((e.id for e in entries), default=0) + 1
    entry = PlanEntry(entry_id, dish, serve_time)
    entries.append(entry)
    return entry


def cancel_plan_entry(entries: List[PlanEntry], entry_id: int) -> bool:
    """Найти запись по id и отменить её; вернуть True при успехе."""
    for entry in entries:
        if entry.id == entry_id:
            entry.cancel()
            return True
    return False


def find_conflicts(
    entries: List[PlanEntry],
) -> List[Tuple[PlanEntry, PlanEntry]]:
    """Найти пары активных записей с пересекающимися активными задачами."""
    active = [e for e in entries if not e.is_cancelled]
    conflicts = []
    for i, first in enumerate(active):
        for second in active[i + 1:]:
            if _has_overlap(
                first.active_intervals(), second.active_intervals(),
            ):
                conflicts.append((first, second))
    return conflicts


def show_entries(entries: List[PlanEntry]) -> None:
    """Вывести список записей плана, отсортированный по началу."""
    for entry in sorted(entries, key=lambda e: e.start_time):
        print(entry)
