import allure
import testit

def shared_step(name: str):
    with allure.step(name):
        with testit.step(name):
            yield

def shared_title(name: str):
    def decorator(func):
        func = allure.title(name)(func)
        func = testit.displayName(name)(func)
        return func
    return decorator