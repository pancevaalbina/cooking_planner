"""Классы предметной области: задача рецепта, рецепт, блюдо."""
from __future__ import annotations

from datetime import timedelta
from typing import List


class Task:
    """Задача рецепта. Базовый класс для активных и пассивных задач."""

    requires_cook = True  # переопределяется в наследниках (полиморфизм)

    def __init__(self, title: str, minutes: int) -> None:
        """Создать задачу с названием и длительностью в минутах."""
        self.title = title
        self.minutes = minutes

    @staticmethod
    def validate_minutes(minutes: int) -> bool:
        """Проверить корректность длительности задачи."""
        return minutes > 0

    @property
    def duration(self) -> timedelta:
        """Длительность задачи как timedelta."""
        return timedelta(minutes=self.minutes)

    def describe(self) -> str:
        """Текстовое описание задачи (переопределяется в наследниках)."""
        return f"{self.title} ({self.minutes} мин)"

    def __str__(self) -> str:
        """Строковое представление задачи."""
        return self.describe()

    def to_dict(self) -> dict:
        """Преобразовать задачу в словарь для сохранения в JSON."""
        return {"title": self.title, "minutes": self.minutes,
                "active": self.requires_cook}

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создать задачу нужного типа (Active/Passive) из данных JSON."""
        task_class = ActiveTask if data["active"] else PassiveTask
        return task_class(data["title"], data["minutes"])


class ActiveTask(Task):
    """Задача, требующая присутствия повара (нарезка, жарка, сборка)."""

    requires_cook = True

    def describe(self) -> str:
        """Переопределенное описание: задача активная."""
        return f"{self.title} ({self.minutes} мин, повар занят)"


class PassiveTask(Task):
    """Задача без участия повара (запекание, варка, охлаждение)."""

    requires_cook = False

    def describe(self) -> str:
        """Переопределенное описание: задача пассивная."""
        return f"{self.title} ({self.minutes} мин, без участия повара)"


class Recipe:
    """Рецепт блюда: описание и упорядоченный список задач.

    Recipe и Task связаны отношением композиции: задачи не существуют
    отдельно от своего рецепта.
    """

    def __init__(self, description: str = "") -> None:
        """Создать рецепт с текстовым описанием и пустым списком задач."""
        self.description = description
        self._tasks: List[Task] = []

    @property
    def tasks(self) -> List[Task]:
        """Вернуть копию списка задач рецепта."""
        return list(self._tasks)

    def add_task(self, task: Task) -> None:
        """Добавить задачу в конец рецепта."""
        self._tasks.append(task)

    @property
    def total_minutes(self) -> int:
        """Общая длительность рецепта в минутах."""
        return sum(task.minutes for task in self._tasks)

    @property
    def active_minutes(self) -> int:
        """Суммарное время, когда повар лично занят рецептом."""
        return sum(t.minutes for t in self._tasks if t.requires_cook)


class Dish:
    """Блюдо: название, количество порций и рецепт приготовления."""

    def __init__(self, dish_id: int, name: str, servings: int,
                 recipe: Recipe | None = None) -> None:
        """Создать блюдо; сохранить переданные данные в атрибутах."""
        if not self.validate_servings(servings):
            raise ValueError("Количество порций должно быть положительным")
        self.id = dish_id
        self.name = name
        self.servings = servings
        self.recipe = recipe if recipe is not None else Recipe()

    @staticmethod
    def validate_servings(servings: int) -> bool:
        """Проверить корректность количества порций."""
        return servings > 0

    @property
    def total_time(self) -> timedelta:
        """Общее время приготовления блюда."""
        return timedelta(minutes=self.recipe.total_minutes)

    def __str__(self) -> str:
        """Строковое представление блюда для вывода пользователю."""
        return (f"{self.id}. {self.name} ({self.servings} порц., "
                f"{self.recipe.total_minutes} мин)")

    def to_dict(self) -> dict:
        """Преобразовать блюдо (с рецептом) в структуру для JSON."""
        return {"id": self.id, "name": self.name,
                "servings": self.servings,
                "recipe": self.recipe.description,
                "tasks": [task.to_dict() for task in self.recipe.tasks]}

    @classmethod
    def from_dict(cls, data: dict) -> "Dish":
        """Восстановить блюдо (с рецептом и задачами) из данных JSON."""
        recipe = Recipe(data.get("recipe", ""))
        for task_data in data["tasks"]:
            recipe.add_task(Task.from_dict(task_data))
        return cls(data["id"], data["name"], data["servings"], recipe)


def add_dish(dishes: List[Dish], name: str, servings: int) -> Dish:
    """Создать объект Dish, добавить его в коллекцию и вернуть его."""
    dish_id = max((d.id for d in dishes), default=0) + 1
    dish = Dish(dish_id, name, servings)
    dishes.append(dish)
    return dish


def find_dish(dishes: List[Dish], dish_id: int) -> Dish | None:
    """Найти блюдо по идентификатору."""
    for dish in dishes:
        if dish.id == dish_id:
            return dish
    return None


def find_dishes_by_name(dishes: List[Dish], query: str) -> List[Dish]:
    """Найти блюда по подстроке названия (без учета регистра)."""
    query = query.lower()
    return [d for d in dishes if query in d.name.lower()]


def filter_dishes_by_time(dishes: List[Dish], max_minutes: int) -> List[Dish]:
    """Отобрать блюда, готовящиеся не дольше max_minutes."""
    return list(d for d in dishes
                if d.recipe.total_minutes <= max_minutes)


def sort_dishes(dishes: List[Dish]) -> List[Dish]:
    """Отсортировать блюда по общему времени приготовления."""
    return sorted(dishes, key=lambda d: d.recipe.total_minutes)


def show_dishes(dishes: List[Dish]) -> None:
    """Вывести список блюд."""
    for dish in sort_dishes(dishes):
        print(dish)
