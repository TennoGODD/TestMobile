#content_page.py

from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as By


class ContentPage(BasePage):
    SETTINGS_BUTTON = (By.ACCESSIBILITY_ID, 'Настройки')
    CODE_INFORMATION_BUTTON = (By.ACCESSIBILITY_ID, 'Информация по коду')
    SERIALIZATION_BUTTON = (By.ACCESSIBILITY_ID, 'Сериализация')

    def tap_settings_button(self):
        self.tap(self.SETTINGS_BUTTON)

    def tap_code_information_button(self):
        self.tap(self.CODE_INFORMATION_BUTTON)

    def tap_code_serialization_button(self):
        self.tap(self.CODE_INFORMATION_BUTTON)



