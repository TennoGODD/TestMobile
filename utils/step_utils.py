import allure
import testit

import functools

def shared_step(name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with allure.step(name):
                with testit.step(name):
                    return func(*args, **kwargs)
        return wrapper
    return decorator

def shared_title(name: str):
    def decorator(func):
        func = allure.title(name)(func)
        func = testit.displayName(name)(func)
        return func
    return decorator