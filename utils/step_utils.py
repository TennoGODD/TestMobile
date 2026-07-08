import allure
import testit
import functools

class shared_step:

    def __init__(self, name: str):
        self.name = name
        # Создаём контекстные менеджеры allure и testit заранее
        self.allure_cm = allure.step(name)
        self.testit_cm = testit.step(name)

    def __enter__(self):
        self.allure_cm.__enter__()
        self.testit_cm.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.testit_cm.__exit__(exc_type, exc_val, exc_tb)
        self.allure_cm.__exit__(exc_type, exc_val, exc_tb)
        return False  # не подавляем исключения

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

def shared_title(name: str):
    def decorator(func):
        func = allure.title(name)(func)
        func = testit.displayName(name)(func)
        return func
    return decorator