"""Планировщик приготовления нескольких блюд (ПР2)."""
from dishes import (add_dish, add_task, find_dish, get_total_time,
                    sort_dishes)
from planner import (add_to_plan, build_schedule, find_conflicts,
                     get_statistics, remove_from_plan)
from storage import load_dishes, load_plan, save_dishes, save_plan
from utils import format_duration, input_datetime, input_int

DISHES_FILE = "data/dishes.json"
PLAN_FILE = "data/plan.json"

MENU = """
=== Планировщик приготовления блюд ===
1. Показать блюда
2. Найти блюдо по названию
3. Добавить блюдо
4. Добавить задачу в рецепт
5. Добавить блюдо в план
6. Убрать блюдо из плана
7. Показать расписание
8. Статистика
0. Выход"""


def show_dishes(dishes: list[dict]) -> None:
    """Вывести список блюд."""
    for dish in sort_dishes(dishes):
        total = format_duration(get_total_time(dish))
        print(f"{dish['id']}. {dish['name']} "
              f"({dish['servings']} порц., {total})")


def show_schedule(dishes: list[dict], plan: list[dict]) -> None:
    """Вывести расписание и конфликты."""
    schedule = build_schedule(dishes, plan)
    if not schedule:
        print("План пуст.")
        return
    for item in schedule:
        kind = "активно" if item["active"] else "пассивно"
        print(f"{item['start']:%H:%M}-{item['end']:%H:%M} "
              f"{item['dish']}: {item['task']} ({kind})")
    for first, second in find_conflicts(schedule):
        print(f"! Конфликт: «{first['task']}» ({first['dish']}) и "
              f"«{second['task']}» ({second['dish']}) пересекаются")


def main() -> None:
    """Точка запуска: цикл меню."""
    dishes = load_dishes(DISHES_FILE)
    plan = load_plan(PLAN_FILE)
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_dishes(dishes)
            elif choice == "2":
                found = find_dish(dishes, input("Название: "))
                show_dishes(found)
            elif choice == "3":
                name = input("Название блюда: ")
                add_dish(dishes, name, input_int("Порций: "))
            elif choice == "4":
                show_dishes(dishes)
                dish_id = input_int("ID блюда: ")
                title = input("Задача: ")
                minutes = input_int("Минут: ")
                active = input("Активная задача? (д/н): ") == "д"
                add_task(dishes, dish_id, title, minutes, active)
            elif choice == "5":
                show_dishes(dishes)
                dish_id = input_int("ID блюда: ")
                add_to_plan(plan, dishes, dish_id,
                            input_datetime("Время подачи: "))
            elif choice == "6":
                if not remove_from_plan(plan, input_int("ID записи: ")):
                    print("Запись не найдена.")
            elif choice == "7":
                show_schedule(dishes, plan)
            elif choice == "8":
                stats = get_statistics(dishes, plan)
                print(f"Блюд в плане: {stats['dishes']}, всего: "
                      f"{format_duration(stats['total_minutes'])}, "
                      f"из них активно: "
                      f"{format_duration(stats['active_minutes'])}, "
                      f"самое долгое: {stats['longest']}")
            elif choice == "0":
                break
            else:
                print("Неизвестная команда.")
        except ValueError as error:
            print(f"Ошибка: {error}")
        save_dishes(DISHES_FILE, dishes)
        save_plan(PLAN_FILE, plan)


if __name__ == "__main__":
    main()
