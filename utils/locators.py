# locators.py

from appium.webdriver.common.appiumby import AppiumBy as By


def escape_uiautomator_text(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"', '\\"')


def by_text(text: str, instance: int = None):
    selector = f'new UiSelector().text("{escape_uiautomator_text(text)}")'
    if instance is not None:
        selector += f'.instance({instance})'
    return (By.ANDROID_UIAUTOMATOR, selector)


def by_text_contains(text: str):
    return (By.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{escape_uiautomator_text(text)}")')


def by_desc(text: str):
    return (By.ACCESSIBILITY_ID, text)
