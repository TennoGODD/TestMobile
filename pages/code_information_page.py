#code_information_page.py

from utils.locators import by_text, by_desc
from utils.step_utils import shared_step
from base.base_page import BasePage


class CodeInformationPage(BasePage):
    MENU_BUTTON = by_desc("Информация по коду")
    PAGE_TITLE = by_text("Отсканируйте, код маркировки для получения информации по нему")
    SECTION_NAME = "Информация по коду"

    CLOSE_BUTTON = by_desc("ЗАКРЫТЬ")

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
            with shared_step(f"Проверка поля '{label}'"):
                prefix = LABEL_PREFIX[label]
                expected_text = f"{prefix}{value}"

                locator = by_text(expected_text)

                self.scroll_to_element(locator, max_swipes=2)
                if not self.is_displayed(locator):
                    raise AssertionError(f"Поле '{label}' не отображается на экране")

                actual_text = self.get_text(locator)
                if actual_text != expected_text:
                    raise AssertionError(
                        f"Поле '{label}': ожидалось '{expected_text}', получено '{actual_text}'"
                    )

        self.scroll_to_element(self.CLOSE_BUTTON, max_swipes=2)
        if not self.is_displayed(self.CLOSE_BUTTON):
            raise AssertionError("Кнопка 'Закрыть' не отображается на экране")
