"""Декораторы проекта."""
from functools import wraps


def log_call(func):
    """Напечатать имя вызываемой функции (для отладки и демонстрации)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[log] вызов {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
