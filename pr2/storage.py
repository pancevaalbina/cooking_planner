"""Загрузка и сохранение данных в JSON."""
import json


def load_json(filename: str) -> list:
    """Прочитать список из JSON-файла; при ошибке вернуть пустой."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустых данных.")
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, начинаем с пустых данных.")
    return []


def save_json(filename: str, data: list) -> None:
    """Записать список в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


def load_dishes(filename: str) -> list[dict]:
    """Загрузить блюда."""
    return load_json(filename)


def save_dishes(filename: str, dishes: list[dict]) -> None:
    """Сохранить блюда."""
    save_json(filename, dishes)


def load_plan(filename: str) -> list[dict]:
    """Загрузить план."""
    return load_json(filename)


def save_plan(filename: str, plan: list[dict]) -> None:
    """Сохранить план."""
    save_json(filename, plan)
