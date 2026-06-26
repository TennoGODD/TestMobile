#code_information_page.py

from utils.step_utils import shared_step
import shlex
from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as By


class CodeInformationPage(BasePage):

    WARNING_FIELD_1 = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Введите адрес сервера, для продложения работы")')
    WARNING_FIELD_2 = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Внимание! Не удалось подключиться к серверу!")')

    CONTENT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(2)')

    PRODUCT_NAME = (By.ID, "com.dmc_mobile:id/product_name")
    PRODUCT_GTIN = (By.ID, "com.dmc_mobile:id/product_gtin")
    PRODUCT_LIFETIME = (By.ID, "com.dmc_mobile:id/product_lifetime")

    @shared_step("Закрыть предупреждение")
    def tap_warning_if_present(self, timeout=2):
        if self.is_displayed(self.WARNING_FIELD_1, timeout=timeout):
            self.tap(self.WARNING_FIELD_1)
        if self.is_displayed(self.WARNING_FIELD_2, timeout=timeout):
            self.tap(self.WARNING_FIELD_2)

    @shared_step("Открыть меню разделов")
    def tap_content_button(self):
        self.tap(self.CONTENT_BUTTON)

    @shared_step("Сканирование кода {barcode}")
    def emulate_scan(self, barcode: str):
        safe_barcode = shlex.quote(barcode)
        cmd = f"am broadcast -a com.android.scanner.broadcast --es scandata {safe_barcode}"
        self.driver.execute_script("mobile: shell", {"command": cmd})

    @shared_step("Проверить поле '{label}' на соответствие ожидаемому значению")
    def _check_field(self, locator, expected_text, label):
        if not self.is_displayed(locator):
            raise AssertionError(f"Поле '{label}' не отображается на экране")
        actual_text = self.get_text(locator).strip()
        expected_text = expected_text.strip()
        if actual_text != expected_text:
            raise AssertionError(
                f"Поле '{label}': ожидалось '{expected_text}', получено '{actual_text}'"
            )

    @shared_step("Проверить информацию после сканирования кода")
    def verify_scanned_data(
            self,
            code=None,  # значение кода
            aggr_info=None,  # информация в агрегате
            gtin=None,  # GTIN
            product_name=None,  # наименование продукции
            status=None,  # статус
            crpt_status=None,  # статус ЦРПТ
            production_date=None,  # дата производства
            serialization_date=None,  # дата сериализации
            emission_date=None,  # дата эмиссии
            task_number=None,  # номер задания
            task_date=None,  # дата задания
            task_status=None,  # статус задания
    ):

        LABEL_PREFIX = {
            "код": "Код: ",
            "информация в агрегате": " ",  # ← ведущий пробел
            "gtin": "GTIN: ",
            "наименование продукции": "Продукция: ",
            "статус": "Статус: ",
            "статус ЦРПТ": "Статус ЦРПТ: ",
            "дата производства": "Дата производства: ",
            "дата сериализации": "Дата сериализации: ",
            "дата эмиссии": "Дата эмиссии: ",
            "номер задания": "Номер задания: ",
            "дата задания": "Дата задания: ",
            "статус задания": "Статус задания: ",
        }

        fields = {
            "код": code,
            "информация в агрегате": aggr_info,
            "gtin": gtin,
            "наименование продукции": product_name,
            "статус": status,
            "статус ЦРПТ": crpt_status,
            "дата производства": production_date,
            "дата сериализации": serialization_date,
            "дата эмиссии": emission_date,
            "номер задания": task_number,
            "дата задания": task_date,
            "статус задания": task_status,
        }

        for label, value in fields.items():
            if value is None:
                continue

            prefix = LABEL_PREFIX[label]
            expected_text = f"{prefix}{value}"

            locator = (By.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{expected_text}")')

            self.scroll_to_element(locator, max_swipes=2)
            if not self.is_displayed(locator):
                raise AssertionError(f"Поле '{label}' не отображается на экране")

            actual_text = self.get_text(locator)
            if actual_text != expected_text:
                raise AssertionError(
                    f"Поле '{label}': ожидалось '{expected_text}', получено '{actual_text}'"
                )

        close_button = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().description("ЗАКРЫТЬ")')
        self.scroll_to_element(close_button, max_swipes=2)
        if not self.is_displayed(close_button):
            raise AssertionError("Кнопка 'Закрыть' не отображается на экране")
