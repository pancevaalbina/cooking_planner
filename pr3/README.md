# Планировщик приготовления нескольких блюд

Консольное приложение для планирования готовки нескольких блюд к одному
времени подачи. Проект продолжает ПР1 и ПР2: с ПР3 предметная область
представлена не словарями и функциями, а классами и объектами.

Приложение позволяет:
* просматривать и искать блюда;
* добавлять новые блюда;
* добавлять записи плана (блюдо + время подачи);
* отменять записи плана;
* показывать план приготовления и конфликты по времени.

## Целевая аудитория
Домашние повара, которые готовят несколько блюд к одному времени
(праздничный стол, обед из нескольких блюд).

## Предметная область
Основные сущности: блюдо (с рецептом из задач) и запись плана,
связывающая блюдо со временем подачи. Пользователь может запланировать
несколько блюд так, чтобы они были готовы к одному моменту; программа
проверяет, что активные (требующие присутствия повара) задачи разных
блюд не пересекаются по времени.

## Основные классы

### Task (и наследники ActiveTask, PassiveTask)
Задача рецепта.
- **Атрибуты:** `title`, `minutes`.
- **Атрибут класса** `requires_cook` — переопределяется в наследниках
  (полиморфизм): `True` у `ActiveTask`, `False` у `PassiveTask`.
- **Методы:** `describe()` (переопределен в наследниках), `__str__()`,
  `to_dict()`; `validate_minutes()` — `@staticmethod`;
  `from_dict()` — `@classmethod`, создает `ActiveTask` или `PassiveTask`
  в зависимости от данных.

### Recipe
Рецепт блюда: описание и список задач.
- **Атрибуты:** `description`, список задач (инкапсулирован в
  `_tasks`, доступен через свойство `tasks`).
- **Методы/свойства:** `add_task()`, `total_minutes`, `active_minutes`.
- Recipe и Task связаны **композицией**: задача не существует отдельно
  от своего рецепта.

### Dish
Блюдо.
- **Атрибуты:** `id`, `name`, `servings`, `recipe` (объект `Recipe`).
- **Методы:** `validate_servings()` — `@staticmethod`; свойство
  `total_time`; `__str__()`; `to_dict()` / `from_dict()`
  (`@classmethod`).
- Dish и Recipe также связаны композицией.

### PlanEntry
Запись плана: блюдо, время подачи, статус.
- **Атрибуты:** `id`, `dish` (объект `Dish`, а не только id — как
  `Booking.room` в методичке), `serve_time`, `is_cancelled`.
- **Методы:** свойство `start_time`; `cancel()` — не удаляет запись,
  а меняет её состояние; `active_intervals()`; `__str__()`,
  учитывающий состояние (активна/отменена).

## Судьба функций ПР2 (аналог таблицы 5.4.3 методички)

| Модуль ПР2 | Функция ПР2 | Что произошло в ПР3 |
|---|---|---|
| dishes.py | `add_dish()` | адаптирована: создает объект `Dish` |
| dishes.py | `find_dish()` | разделена на `find_dish(by id)` и `find_dishes_by_name()` |
| dishes.py | `get_total_time()` | перенесена в `Dish.recipe.total_minutes` / `Dish.total_time` |
| dishes.py | `filter_dishes_by_time()` | адаптирована для `List[Dish]` |
| dishes.py | `sort_dishes()` | адаптирована для `List[Dish]` (lambda сохранена) |
| planner.py | `calculate_start_time()` | перенесена в `PlanEntry.start_time` |
| planner.py | `is_time_free` (аналог `is_room_available`) | адаптирована: проверяет пересечение активных задач |
| planner.py | `add_to_plan()` | переработана в `create_plan_entry()`, возвращает `Optional[PlanEntry]` |
| planner.py | `remove_from_plan()` | заменена на `cancel_plan_entry()` — запись не удаляется, а помечается отмененной |
| planner.py | `get_start_status()` | **перенесена без изменений** (функция из ПР1) |
| planner.py | `find_conflicts()` | адаптирована для объектов `PlanEntry` |
| storage.py | `load_dishes/save_dishes` | адаптированы: JSON ⇄ объекты `Dish` |
| storage.py | `load_plan/save_plan` | адаптированы: восстанавливают ссылку `PlanEntry.dish` по `dish_id` |
| utils.py | `input_int`, `input_datetime` | остались обычными функциями (не относятся к объектам) |

## Взаимодействие объектов
```
PlanEntry
 └── dish -> Dish
              └── recipe -> Recipe
                             └── tasks -> [Task, ...]
```
`PlanEntry` хранит прямую ссылку на объект `Dish` (а не его id), поэтому
`entry.dish.name`, `entry.dish.recipe.total_minutes` и т. п. доступны
напрямую. Идентификатор (`dish_id`) используется только в JSON.

## Хранение данных
Данные хранятся в JSON (как и в ПР2):
- `data/dishes.json` — список блюд с рецептами;
- `data/plan.json` — список записей плана (`dish_id`, `serve_time`,
  `is_cancelled`).

При загрузке JSON преобразуется в объекты (`Dish.from_dict`,
`PlanEntry` с восстановленной ссылкой на блюдо); при сохранении —
обратно в структуры JSON.

## Структура проекта
```text
pr3/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── decorators.py
├── storage.py
├── utils.py
├── models/
│   ├── __init__.py
│   ├── dishes.py      # Task, ActiveTask, PassiveTask, Recipe, Dish
│   └── plan.py        # PlanEntry
├── data/
│   ├── dishes.json
│   └── plan.json
└── tests/
    ├── test_dishes.py
    └── test_plan.py
```

## Запуск программы
```
python main.py
```

## Запуск тестов
```
pytest -v
```

## Проверка качества кода
```
flake8 .
```

## Git
Проект продолжает репозиторий, созданный в ПР1 и доработанный в ПР2:
отдельный репозиторий для ПР3 не создается. Коммиты начинаются с
метки `PR3:`, например:
```
PR3: add Dish/Task/Recipe classes
PR3: replace remove_from_plan with cancel_plan_entry
PR3: adapt tests to object model
```

## План развития
- разработка веб-приложения на Django;
- подключение базы данных;
- реализация пользователей (авторизация появится позже, на ПР11);
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
