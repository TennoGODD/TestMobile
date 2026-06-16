#content_page.py

from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as By


class ContentPage(BasePage):
    SETTINGS_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Настройки")')
    CODE_INFORMATION_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Информация по коду")')

    def tap_settings_button(self):
        self.tap(self.SETTINGS_BUTTON)

    def tap_code_information_button(self):
        self.tap(self.CODE_INFORMATION_BUTTON)


