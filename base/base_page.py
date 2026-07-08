#base_page.py

import shlex

from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.locators import by_text
from utils.step_utils import shared_step


class BasePage:
    CONTENT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(2)')

    WARNING_FIELD_1 = by_text("Введите адрес сервера, для продолжения работы")
    WARNING_FIELD_2 = by_text("Внимание! Не удалось подключиться к серверу!")
    WARNING_FIELD_3 = by_text("Request failed with status code 422")

    MENU_BUTTON = None    
    PAGE_TITLE = None     
    SECTION_NAME = None   

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def tap(self, locator):
        el = self.find_element(locator)
        self.scroll_to_element(locator)
        el.click()

    def input_text(self, locator, text):
        el = self.find_element(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def is_displayed(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @shared_step("Открыть меню разделов")
    def tap_content_button(self):
        self.tap(self.CONTENT_BUTTON)

    @shared_step("Закрыть предупреждение")
    def tap_warning_if_present(self, timeout=2):
        if self.is_displayed(self.WARNING_FIELD_1, timeout=timeout):
            self.tap(self.WARNING_FIELD_1)
        if self.is_displayed(self.WARNING_FIELD_2, timeout=timeout):
            self.tap(self.WARNING_FIELD_2)
        if self.is_displayed(self.WARNING_FIELD_3, timeout=timeout):
            self.tap(self.WARNING_FIELD_3)

    def emulate_scan(self, barcode: str):
        with shared_step(f"Сканирование кода {barcode}"):
            safe_barcode = shlex.quote(barcode)
            cmd = f"am broadcast -a com.android.scanner.broadcast --es scandata {safe_barcode}"
            self.driver.execute_script("mobile: shell", {"command": cmd})

    def swipe_down(self, force=0.5, duration=300):
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        force = max(0.0, min(1.0, force))
        start_y = int(size['height'] * (0.8 - 0.3 * force))
        end_y = int(size['height'] * (0.3 + 0.2 * force))
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_up(self, force=0.5, duration=300):
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        force = max(0.0, min(1.0, force))
        start_y = int(size['height'] * (0.3 + 0.2 * force))
        end_y = int(size['height'] * (0.8 - 0.3 * force))
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)

    def scroll_to_element(self, locator, max_swipes=10, timeout=2):
        return self._scroll_until_visible(locator, max_swipes, timeout, direction="down")

    def scroll_to_element_up(self, locator, max_swipes=10, timeout=2):
        return self._scroll_until_visible(locator, max_swipes, timeout, direction="up")

    def _scroll_until_visible(self, locator, max_swipes, timeout, direction):
        if self.is_displayed(locator, timeout=timeout):
            return self.find_element(locator)

        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        if direction == "down":
            start_y, end_y = int(size["height"] * 0.7), int(size["height"] * 0.3)
        else:
            start_y, end_y = int(size["height"] * 0.2), int(size["height"] * 0.8)

        for _ in range(max_swipes):
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                return self.driver.find_element(*locator)
            except TimeoutException:
                self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)

        raise TimeoutException(f"Элемент {locator} не найден после {max_swipes} свайпов ({direction})")
