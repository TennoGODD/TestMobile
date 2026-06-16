#code_information_page.py

import allure
import shlex
from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as By


class CodeInformationPage(BasePage):

    WARNING_FIELD_1 = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Введите адрес сервера, для продложения работы")')
    WARNING_FIELD_2 = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Внимание! Не удалось подключиться к серверу!")')

    CONTENT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(1)')

    PRODUCT_NAME = (By.ID, "com.dmc_mobile:id/product_name")
    PRODUCT_GTIN = (By.ID, "com.dmc_mobile:id/product_gtin")
    PRODUCT_LIFETIME = (By.ID, "com.dmc_mobile:id/product_lifetime")

    @allure.step("Закрыть предупреждение")
    def tap_warning_if_present(self, timeout=2):
        if self.is_displayed(self.WARNING_FIELD_1, timeout=timeout):
            self.tap(self.WARNING_FIELD_1)
        if self.is_displayed(self.WARNING_FIELD_2, timeout=timeout):
            self.tap(self.WARNING_FIELD_2)

    @allure.step("Открыть меню разделов")
    def tap_content_button(self):
        self.tap(self.CONTENT_BUTTON)

    @allure.step("Сканирование кода {barcode}")
    def emulate_scan(self, barcode: str):
        safe_barcode = shlex.quote(barcode)
        cmd = f"am broadcast -a com.android.scanner.broadcast --es scandata {safe_barcode}"
        self.driver.execute_script("mobile: shell", {"command": cmd})
