"""Работа с блюдами, рецептами и задачами."""


def get_dish(dishes: list[dict], dish_id: int) -> dict | None:
    """Вернуть блюдо по идентификатору или None."""
    for dish in dishes:
        if dish["id"] == dish_id:
            return dish
    return None


def add_dish(dishes: list[dict], name: str, servings: int,
             recipe: str = "") -> dict:
    """Добавить блюдо в список и вернуть его."""
    if servings <= 0:
        raise ValueError("Количество порций должно быть положительным")
    dish_id = max((d["id"] for d in dishes), default=0) + 1
    dish = {"id": dish_id, "name": name, "servings": servings,
            "recipe": recipe, "tasks": []}
    dishes.append(dish)
    return dish


def add_task(dishes: list[dict], dish_id: int, title: str,
             minutes: int, active: bool) -> dict:
    """Добавить задачу в рецепт блюда."""
    dish = get_dish(dishes, dish_id)
    if dish is None:
        raise ValueError(f"Блюдо {dish_id} не найдено")
    if minutes <= 0:
        raise ValueError("Длительность задачи должна быть положительной")
    task = {"title": title, "minutes": minutes, "active": active}
    dish["tasks"].append(task)
    return task


def find_dish(dishes: list[dict], query: str) -> list[dict]:
    """Найти блюда по подстроке названия (без учета регистра)."""
    query = query.lower()
    return [d for d in dishes if query in d["name"].lower()]


def get_total_time(dish: dict) -> int:
    """Общее время приготовления блюда в минутах."""
    total = 0
    for task in dish["tasks"]:
        total += task["minutes"]
    return total


def get_active_time(dish: dict) -> int:
    """Время, когда повар занят блюдом лично."""
    return sum(t["minutes"] for t in dish["tasks"] if t["active"])


def filter_dishes_by_time(dishes: list[dict], max_minutes: int) -> list[dict]:
    """Отобрать блюда, готовящиеся не дольше max_minutes."""
    return list(d for d in dishes if get_total_time(d) <= max_minutes)


def sort_dishes(dishes: list[dict]) -> list[dict]:
    """Отсортировать блюда по общему времени приготовления."""
    return sorted(dishes, key=lambda d: get_total_time(d))
