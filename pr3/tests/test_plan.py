from datetime import datetime

from models import ActiveTask, Dish, PassiveTask, Recipe
from models.plan import (cancel_plan_entry, create_plan_entry,
                         find_conflicts, get_start_status, is_time_free)

SERVE = datetime(2026, 9, 20, 19, 0)


def make_dishes():
    chicken_recipe = Recipe("Курица")
    chicken_recipe.add_task(ActiveTask("Подготовка", 20))
    chicken_recipe.add_task(PassiveTask("Духовка", 75))
    salad_recipe = Recipe("Салат")
    salad_recipe.add_task(ActiveTask("Нарезка", 20))
    return [Dish(1, "Курица", 4, chicken_recipe),
            Dish(2, "Салат", 2, salad_recipe)]


def test_dish_finishes_at_serve_time():
    dishes = make_dishes()
    entries = []
    entry = create_plan_entry(entries, dishes, 1, SERVE)
    assert entry.serve_time == SERVE
    assert entry.start_time == datetime(2026, 9, 20, 17, 25)


def test_no_conflict_when_active_windows_differ():
    # Курица: активна 17:25-17:45 (потом духовка). Салат: активна 18:40-19:00.
    # Активные окна не пересекаются - конфликта быть не должно.
    dishes = make_dishes()
    entries = []
    create_plan_entry(entries, dishes, 1, SERVE)
    create_plan_entry(entries, dishes, 2, SERVE)
    assert find_conflicts(entries) == []


def test_conflict_when_active_windows_overlap():
    # Оба блюда подаются в один момент и оба активны прямо перед подачей.
    dishes = make_dishes()
    entries = []
    create_plan_entry(entries, dishes, 2, SERVE)
    salad_2 = Dish(3, "Ещё салат", 2, dishes[1].recipe)
    dishes.append(salad_2)
    entry = create_plan_entry(entries, dishes, 3, SERVE)
    assert entry is None  # is_time_free должно было это предотвратить
    assert len(find_conflicts(entries)) == 0  # т.к. вторая запись не создана


def test_conflict_detected_for_overlapping_active_tasks():
    dishes = make_dishes()
    entries = []
    create_plan_entry(entries, dishes, 2, datetime(2026, 9, 20, 18, 50))
    is_free = is_time_free(entries, dishes[1], datetime(2026, 9, 20, 18, 55))
    assert not is_free


def test_create_returns_none_on_conflict():
    dishes = make_dishes()
    entries = []
    create_plan_entry(entries, dishes, 2, SERVE)
    second = create_plan_entry(entries, dishes, 2, SERVE)
    assert second is None


def test_cancel_does_not_delete_and_frees_time():
    dishes = make_dishes()
    entries = []
    first = create_plan_entry(entries, dishes, 2, SERVE)
    assert cancel_plan_entry(entries, first.id)
    assert first in entries
    assert first.is_cancelled
    second = create_plan_entry(entries, dishes, 2, SERVE)
    assert second is not None


def test_get_start_status_unchanged_from_pr1():
    now = datetime(2026, 9, 20, 16, 0)
    late = datetime(2026, 9, 20, 15, 0)
    assert get_start_status(late, now).startswith("Опаздываем")
