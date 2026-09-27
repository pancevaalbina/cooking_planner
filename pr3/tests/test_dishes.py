import pytest

from models import ActiveTask, Dish, PassiveTask, Recipe, Task
from models.dishes import (add_dish, filter_dishes_by_time,
                           find_dishes_by_name, sort_dishes)


def make_dish(dish_id, name, active_min, passive_min):
    recipe = Recipe(f"Рецепт {name}")
    recipe.add_task(ActiveTask("Подготовка", active_min))
    if passive_min:
        recipe.add_task(PassiveTask("Готовка", passive_min))
    return Dish(dish_id, name, 4, recipe)


def test_dish_creation_and_str():
    dish = make_dish(1, "Борщ", 20, 60)
    assert dish.id == 1
    assert dish.name == "Борщ"
    assert "Борщ" in str(dish)


def test_dish_invalid_servings():
    with pytest.raises(ValueError):
        Dish(1, "Салат", 0)


def test_task_invalid_minutes_via_static_validator():
    assert not Task.validate_minutes(0)
    assert Task.validate_minutes(5)


def test_polymorphism_requires_cook():
    assert ActiveTask("Нарезка", 10).requires_cook
    assert not PassiveTask("Духовка", 60).requires_cook


def test_polymorphism_describe_differs():
    active = ActiveTask("Нарезка", 10).describe()
    passive = PassiveTask("Духовка", 10).describe()
    assert active != passive


def test_recipe_totals_composition():
    dish = make_dish(1, "Курица", 20, 75)
    assert dish.recipe.total_minutes == 95
    assert dish.recipe.active_minutes == 20


def test_task_from_dict_classmethod():
    task = Task.from_dict({"title": "X", "minutes": 5, "active": True})
    assert isinstance(task, ActiveTask)


def test_add_dish_assigns_id_and_returns_object():
    dishes = []
    dish = add_dish(dishes, "Плов", 4)
    assert dish is dishes[0]
    assert dish.id == 1


def test_find_dishes_by_name_ignores_case():
    dishes = [make_dish(1, "Борщ", 10, 10), make_dish(2, "Салат", 10, 0)]
    assert len(find_dishes_by_name(dishes, "борщ")) == 1


def test_filter_dishes_by_time():
    dishes = [make_dish(1, "Быстро", 10, 0), make_dish(2, "Долго", 10, 200)]
    fast = filter_dishes_by_time(dishes, 30)
    assert [d.name for d in fast] == ["Быстро"]


def test_sort_dishes_by_total_time():
    dishes = [make_dish(1, "Долго", 10, 200), make_dish(2, "Быстро", 10, 0)]
    assert sort_dishes(dishes)[0].name == "Быстро"
