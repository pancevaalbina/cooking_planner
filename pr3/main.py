"""Планировщик приготовления нескольких блюд (ПР3, ООП)."""
from models import Dish, PlanEntry
from models.dishes import add_dish, find_dish, find_dishes_by_name, \
    show_dishes
from models.plan import cancel_plan_entry, create_plan_entry, \
    find_conflicts, show_entries
from storage import load_dishes, load_plan, save_dishes, save_plan
from utils import input_datetime, input_int

DISHES_FILE = "data/dishes.json"
PLAN_FILE = "data/plan.json"

MENU = """
=== Планировщик приготовления блюд ===
1. Показать блюда
2. Найти блюдо по названию
3. Добавить блюдо
4. Добавить запись в план
5. Отменить запись плана
6. Показать план и конфликты
0. Выход"""


def create_new_entry(entries: list[PlanEntry], dishes: list[Dish]) -> None:
    """Пользовательский сценарий: выбрать блюдо и добавить запись плана."""
    show_dishes(dishes)
    dish_id = input_int("ID блюда: ")
    if find_dish(dishes, dish_id) is None:
        print("Блюдо не найдено.")
        return
    serve_time = input_datetime("Время подачи (ДД.ММ.ГГГГ ЧЧ:ММ): ")
    entry = create_plan_entry(entries, dishes, dish_id, serve_time)
    if entry is None:
        print("Не удалось создать запись: конфликт по времени с другим "
              "блюдом.")
        return
    print(f"Запись создана: {entry}")


def main() -> None:
    """Точка запуска: цикл меню приложения."""
    dishes = load_dishes(DISHES_FILE)
    entries = load_plan(PLAN_FILE, dishes)
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_dishes(dishes)
            elif choice == "2":
                show_dishes(find_dishes_by_name(dishes, input("Название: ")))
            elif choice == "3":
                name = input("Название блюда: ")
                add_dish(dishes, name, input_int("Порций: "))
            elif choice == "4":
                create_new_entry(entries, dishes)
            elif choice == "5":
                if not cancel_plan_entry(entries, input_int("ID записи: ")):
                    print("Запись не найдена.")
            elif choice == "6":
                show_entries(entries)
                for first, second in find_conflicts(entries):
                    print(f"! Конфликт: записи {first.id} и {second.id} "
                          "пересекаются по активным задачам")
            elif choice == "0":
                break
            else:
                print("Неизвестная команда.")
        except ValueError as error:
            print(f"Ошибка: {error}")
        save_dishes(DISHES_FILE, dishes)
        save_plan(PLAN_FILE, entries)


if __name__ == "__main__":
    main()
