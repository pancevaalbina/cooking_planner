from datetime import datetime

from dishes import add_dish, add_task
from planner import (add_to_plan, build_schedule, calculate_start_time,
                     find_conflicts, remove_from_plan)

SERVE = datetime(2026, 9, 20, 19, 0)


def make_data():
    dishes = []
    add_dish(dishes, "Курица", 4)
    add_task(dishes, 1, "Подготовка", 20, True)
    add_task(dishes, 1, "Духовка", 75, False)
    add_dish(dishes, "Салат", 2)
    add_task(dishes, 2, "Нарезка", 20, True)
    return dishes


def test_calculate_start_time():
    start = calculate_start_time(make_data()[0], SERVE)
    assert start == datetime(2026, 9, 20, 17, 25)


def test_dishes_finish_together():
    dishes = make_data()
    plan = []
    add_to_plan(plan, dishes, 1, SERVE)
    add_to_plan(plan, dishes, 2, SERVE)
    schedule = build_schedule(dishes, plan)
    assert max(item["end"] for item in schedule) == SERVE


def test_no_conflict_for_single_dish():
    dishes = make_data()
    plan = []
    add_to_plan(plan, dishes, 1, SERVE)
    assert find_conflicts(build_schedule(dishes, plan)) == []


def test_conflict_detected():
    dishes = make_data()
    plan = []
    add_to_plan(plan, dishes, 2, datetime(2026, 9, 20, 18, 50))
    add_to_plan(plan, dishes, 2, datetime(2026, 9, 20, 18, 50))
    assert len(find_conflicts(build_schedule(dishes, plan))) == 1


def test_remove_from_plan():
    dishes = make_data()
    plan = []
    add_to_plan(plan, dishes, 1, SERVE)
    assert remove_from_plan(plan, 1)
    assert not remove_from_plan(plan, 1)
