"""План готовки: время начала, расписание задач, конфликты."""
from datetime import datetime, timedelta

from dishes import get_dish, get_total_time, get_active_time


def add_to_plan(plan: list[dict], dishes: list[dict], dish_id: int,
                serve_time: datetime) -> dict:
    """Добавить блюдо в план с указанным временем подачи."""
    if get_dish(dishes, dish_id) is None:
        raise ValueError(f"Блюдо {dish_id} не найдено")
    entry_id = max((e["id"] for e in plan), default=0) + 1
    entry = {"id": entry_id, "dish_id": dish_id,
             "serve_time": serve_time.isoformat(timespec="minutes")}
    plan.append(entry)
    return entry


def remove_from_plan(plan: list[dict], entry_id: int) -> bool:
    """Удалить запись из плана; вернуть True, если она была."""
    for entry in plan:
        if entry["id"] == entry_id:
            plan.remove(entry)
            return True
    return False


def calculate_start_time(dish: dict, serve_time: datetime) -> datetime:
    """Когда нужно начать блюдо, чтобы подать его в serve_time."""
    return serve_time - timedelta(minutes=get_total_time(dish))


def build_schedule(dishes: list[dict], plan: list[dict]) -> list[dict]:
    """Построить расписание всех задач, отсортированное по началу."""
    schedule = []
    for entry in plan:
        dish = get_dish(dishes, entry["dish_id"])
        if dish is None:
            continue
        serve_time = datetime.fromisoformat(entry["serve_time"])
        current = calculate_start_time(dish, serve_time)
        for task in dish["tasks"]:
            end = current + timedelta(minutes=task["minutes"])
            schedule.append({"dish": dish["name"], "task": task["title"],
                             "start": current, "end": end,
                             "active": task["active"]})
            current = end
    return sorted(schedule, key=lambda item: item["start"])


def find_conflicts(schedule: list[dict]) -> list[tuple[dict, dict]]:
    """Найти пары активных задач, которые пересекаются по времени."""
    active = [item for item in schedule if item["active"]]
    conflicts = []
    for i in range(len(active)):
        for j in range(i + 1, len(active)):
            first, second = active[i], active[j]
            overlap = (first["start"] < second["end"]
                       and second["start"] < first["end"])
            if overlap:
                conflicts.append((first, second))
    return conflicts


def get_start_status(start_time: datetime, now: datetime) -> str:
    """Статус блюда относительно текущего времени (функция из ПР1)."""
    if start_time < now:
        return "Опаздываем: начинать нужно было раньше"
    if start_time == now:
        return "Пора начинать прямо сейчас"
    return "Времени достаточно, можно подождать"


def get_statistics(dishes: list[dict], plan: list[dict]) -> dict:
    """Статистика по плану."""
    planned = [get_dish(dishes, e["dish_id"]) for e in plan]
    planned = [d for d in planned if d is not None]
    stats = {"dishes": len(planned),
             "total_minutes": sum(get_total_time(d) for d in planned),
             "active_minutes": sum(get_active_time(d) for d in planned),
             "longest": None}
    if planned:
        stats["longest"] = max(planned, key=get_total_time)["name"]
    return stats
