# Шпаргалка: Git и отладка

```
git init
git add .
git commit -m "ПР1: стартовый сценарий планировщика"
git status
git log --oneline
git remote add origin <url>
git push -u origin main
```
Рекомендуется один репозиторий cooking-planner: коммиты «ПР1», «ПР2», «ПР3»
(или отдельные папки/ветки). Методичка требует, чтобы в Git сохранялась
версия каждой ПР.

## Отладка (ПР1, п. 6.6)
1. Поставьте breakpoint на строке `start_time = calculate_start_time(...)`.
2. Запустите в режиме Debug, пройдите Step Over / Step Into.
3. Посмотрите `total_minutes`, `serve_time`, `start_time` в окне переменных.
4. Внесите ошибку: в `calculate_start_time` замените `-` на `+`.
   Отладчик покажет, что время начала оказалось позже подачи. Исправьте.
