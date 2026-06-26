#base_page.py
import time

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
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
        except:
            return False

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

        if self.is_displayed(locator, timeout=timeout):
            return self.find_element(locator)

        window_size = self.driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]
        start_x = width // 2
        start_y = int(height * 0.7)
        end_y = int(height * 0.3)
        # start_y = int(height * 0.8)
        # end_y = int(height * 0.2)

        for _ in range(max_swipes):
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                return self.driver.find_element(*locator)
            except TimeoutException:
                self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)

        raise Exception(f"Элемент с локатором {locator} не найден после {max_swipes} свайпов")

    def scroll_to_element_up(self, locator, max_swipes=10, timeout=2):
        if self.is_displayed(locator, timeout=timeout):
            return self.find_element(locator)

        window_size = self.driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]
        start_x = width // 2
        start_y = int(height * 0.2)
        end_y = int(height * 0.8)

        for _ in range(max_swipes):
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                return self.driver.find_element(*locator)
            except TimeoutException:
                self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)

        raise Exception(f"Элемент {locator} не найден после {max_swipes} свайпов вверх")
