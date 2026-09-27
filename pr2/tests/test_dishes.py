import pytest

from dishes import (add_dish, add_task, find_dish, get_total_time,
                    sort_dishes)


def make_dishes():
    dishes = []
    add_dish(dishes, "Борщ", 4)
    add_task(dishes, 1, "Варить", 60, False)
    add_task(dishes, 1, "Нарезать", 15, True)
    add_dish(dishes, "Салат", 2)
    add_task(dishes, 2, "Нарезать", 10, True)
    return dishes


def test_add_dish_assigns_ids():
    dishes = make_dishes()
    assert [d["id"] for d in dishes] == [1, 2]


def test_get_total_time():
    assert get_total_time(make_dishes()[0]) == 75


def test_find_dish_ignores_case():
    assert len(find_dish(make_dishes(), "борщ")) == 1


def test_sort_dishes_by_time():
    assert sort_dishes(make_dishes())[0]["name"] == "Салат"


def test_add_task_unknown_dish():
    with pytest.raises(ValueError):
        add_task([], 5, "Нарезать", 10, True)
