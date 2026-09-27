"""Загрузка и сохранение объектов Dish и PlanEntry в JSON.

Использование классов не отменяет работу с JSON: данные из файлов
преобразуются в объекты (load_*), а перед сохранением объекты
преобразуются обратно в обычные структуры (save_*).
"""
import json
from datetime import datetime
from typing import List

from models.dishes import Dish
from models.plan import PlanEntry


def _read(filename: str) -> list:
    """Прочитать список из JSON-файла; при ошибке вернуть пустой."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустых данных.")
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, начинаем с пустых данных.")
    return []


def _write(filename: str, data: list) -> None:
    """Записать список в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


def load_dishes(filename: str) -> List[Dish]:
    """Загрузить блюда из JSON и создать объекты Dish."""
    return [Dish.from_dict(item) for item in _read(filename)]


def save_dishes(filename: str, dishes: List[Dish]) -> None:
    """Сохранить объекты Dish в JSON."""
    _write(filename, [dish.to_dict() for dish in dishes])


def load_plan(filename: str, dishes: List[Dish]) -> List[PlanEntry]:
    """Загрузить план из JSON, восстановив ссылки на объекты Dish."""
    entries = []
    for item in _read(filename):
        dish = next((d for d in dishes if d.id == item["dish_id"]), None)
        if dish is None:
            continue  # блюдо удалено - запись плана пропускается
        entry = PlanEntry(item["id"], dish,
                          datetime.fromisoformat(item["serve_time"]))
        entry.is_cancelled = item["is_cancelled"]
        entries.append(entry)
    return entries


def save_plan(filename: str, entries: List[PlanEntry]) -> None:
    """Сохранить план в JSON, заменив ссылки на объекты их id."""
    data = [{"id": e.id, "dish_id": e.dish.id,
             "serve_time": e.serve_time.isoformat(timespec="minutes"),
             "is_cancelled": e.is_cancelled} for e in entries]
    _write(filename, data)
