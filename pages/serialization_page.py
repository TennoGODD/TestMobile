#serialization_page.py

from utils.locators import by_text, by_text_contains, by_desc
from utils.step_utils import shared_step
from base.base_page import BasePage


class SerializationPage(BasePage):
    MENU_BUTTON = by_desc("Сериализация")
    PAGE_TITLE = by_text_contains("Отсканируйте код маркировки")
    SECTION_NAME = "Сериализация"

    TASK_WARNING = by_desc('Задание взято в работу при статусе  отличном от "Готов к сериализации на линии". Завершать задание запрещено')

    # Диалог выбора упаковки (агрегации)
    AGGREGATION_DIALOG_TEXT = by_text_contains("Вы хотите произвести агрегацию")
    AGGREGATION_DIALOG_NO_BUTTON = by_text_contains("НЕТ")

    SHOW_PRINT_SETTINGS_BUTTON = by_desc("ПОКАЗАТЬ НАСТРОЙКИ ПЕЧАТИ")
    COLLECT_BUTTON = by_desc("СОБРАТЬ")

    CONFIRM_DIALOG_TEXT = by_text("Задание полностью собрано, завершить?")
    CONFIRM_DIALOG_FINISH_BUTTON = by_desc("ЗАВЕРШИТЬ")
    CONFIRM_DIALOG_RETURN_BUTTON = by_desc("ВЕРНУТЬСЯ")

    FINISH_BUTTON = by_desc("ЗАВЕРШИТЬ")
    ABORT_BUTTON = by_desc("ПРЕРВАТЬ")

    PRINT_DIALOG_TASK_PREFIX = "Задание: "
    PRINT_DIALOG_GTIN_PREFIX = "GTIN: "
    PRINT_BUTTON = by_desc("РАСПЕЧАТАТЬ")

    def emulate_scan_kigu(self, unit_id: str, crypto_tail: str):
        """Сканирование кода КИГУ (агрегат уровня 0).

        На этикетке КИГУ unit_id и криптохвост разделены невидимым символом
        GS (ASCII 29) — сканер передаёт его внутри строки, поэтому добавляем
        его и здесь. Агрегат уровня 1 сканируется обычным emulate_scan.
        """
        self.emulate_scan(f"{unit_id}\x1d{crypto_tail}")

    def select_aggregation_packaging(self, packaging_accessibility_id: str):
        with shared_step(f"Нажать кнопку {packaging_accessibility_id}"):
            locator = by_desc(packaging_accessibility_id)
            self.scroll_to_element(locator, max_swipes=2)
            self.tap(locator)

    def assert_aggregation_dialog_displayed(self):
        if not self.is_displayed(self.AGGREGATION_DIALOG_TEXT):
            raise AssertionError("Диалог 'Вы хотите произвести агрегацию?' не отображается")
        if not self.is_displayed(self.AGGREGATION_DIALOG_NO_BUTTON):
            raise AssertionError("Кнопка 'НЕТ' не отображается в диалоге агрегации")

    @shared_step("Закрыть предупреждение по заданю")
    def tap_task_warning_if_present(self, timeout=3):
        if self.is_displayed(self.TASK_WARNING, timeout=timeout):
            self.tap(self.TASK_WARNING)

    @shared_step("Проверить данные на экране сериализации")
    def verify_serialization_data(
            self,
            task_number=None,
            gtin=None,
            km_status=None,
            product_name=None,
            total_km_label=None,
            verified_km_count=None,
            scanned_in_aggr=None,
            completed_aggr=None,
            check_action_buttons=False,
    ):
        fields = {
            "задание": task_number,
            "gtin": gtin,
            "КМ и статус": km_status,
            "наименование продукции": product_name,
            "общее количество КМ": total_km_label,
            "количество верифицированных КМ": verified_km_count,
            "КМ в агрегате": scanned_in_aggr,
            "завершённые агрегаты": completed_aggr,
        }

        for label, expected_text in fields.items():
            if expected_text is None:
                continue

            locator = by_text(expected_text)

            self.scroll_to_element(locator, max_swipes=2)
            if not self.is_displayed(locator):
                raise AssertionError(f"Поле '{label}' с текстом '{expected_text}' не отображается на экране")

            actual_text = self.get_text(locator)
            if actual_text != expected_text:
                raise AssertionError(
                    f"Поле '{label}': ожидалось '{expected_text}', получено '{actual_text}'"
                )

        if check_action_buttons:
            self.scroll_to_element(self.FINISH_BUTTON, max_swipes=2)
            if not self.is_displayed(self.FINISH_BUTTON):
                raise AssertionError("Кнопка 'ЗАВЕРШИТЬ' не отображается")

            self.scroll_to_element(self.ABORT_BUTTON, max_swipes=2)
            if not self.is_displayed(self.ABORT_BUTTON):
                raise AssertionError("Кнопка 'ПРЕРВАТЬ' не отображается")

    @shared_step('Нажать кнопку “Завершить“')
    def tap_finish_button(self):
        self.scroll_to_element(self.FINISH_BUTTON, max_swipes=2)
        self.tap(self.FINISH_BUTTON)

    @shared_step('Нажать кнопку “Завершить“')
    def confirm_finish_in_dialog(self):
        self.scroll_to_element(self.CONFIRM_DIALOG_FINISH_BUTTON, max_swipes=2)
        self.tap(self.CONFIRM_DIALOG_FINISH_BUTTON)

    @shared_step('Нажать кнопку “Вернуться“')
    def cancel_finish_in_dialog(self):
        self.scroll_to_element(self.CONFIRM_DIALOG_RETURN_BUTTON, max_swipes=2)
        self.tap(self.CONFIRM_DIALOG_RETURN_BUTTON)

    def is_finish_dialog_displayed(self) -> bool:
        return self.is_displayed(self.CONFIRM_DIALOG_TEXT) and \
            self.is_displayed(self.CONFIRM_DIALOG_FINISH_BUTTON) and \
            self.is_displayed(self.CONFIRM_DIALOG_RETURN_BUTTON)

    @shared_step('Открылось предупреждение с текстом “Задание полностью собрано“, кнопками “Завершить“ и “Вернуться“')
    def assert_finish_dialog_displayed(self):
        if not self.is_finish_dialog_displayed():
            raise AssertionError("Диалог 'Задание полностью собрано, завершить?' не отображается")

    def assert_print_control_dialog_displayed(self, task_number: str, gtin: str):
        task_locator = by_text(task_number)
        gtin_locator = by_text(gtin)

        self.scroll_to_element(task_locator, max_swipes=2)
        if not self.is_displayed(task_locator):
            raise AssertionError(f"Номер задания '{task_number}' не отображается в окне печати")

        self.scroll_to_element(gtin_locator, max_swipes=2)
        if not self.is_displayed(gtin_locator):
            raise AssertionError(f"GTIN '{gtin}' не отображается в окне печати")

        self.scroll_to_element(self.PRINT_BUTTON, max_swipes=2)
        if not self.is_displayed(self.PRINT_BUTTON):
            raise AssertionError("Кнопка 'РАСПЕЧАТАТЬ' не отображается в окне печати")

    def tap_print_button(self):
        self.tap(self.PRINT_BUTTON)
