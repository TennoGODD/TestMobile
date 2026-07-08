# settings_page.py
import allure
from utils.step_utils import shared_step

from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as By
from utils.locators import by_text, by_desc


class SettingsPage(BasePage):
    MENU_BUTTON = by_desc("Настройки")
    PAGE_TITLE = by_text("Настройки подключения")
    SECTION_NAME = "Настройки"

    CHECK_CONNECTION_BUTTON = by_text("ПРОВЕРКА СВЯЗИ")
    SUCCESSFUL_CHECK_CONNECTION = by_text("Успешное подключение к серверу!")
    UNSUCCESSFUL_CHECK_CONNECTION = by_text("Ошибка! Подключение к серверу отсутвует!")

    LIST_FIXES_VERSION_BUTTON = by_desc("СПИСОК ИСПРАВЛЕНИЙ ПО ВЕРСИЯМ")

    VERSION_TEXT = (By.XPATH, '//android.widget.TextView[@text="Версия приложения:"]/following-sibling::android.widget.TextView')

    ADDRESS_SERVER_FIELD = (By.XPATH, '//android.widget.TextView[@text="Адрес сервера:"]/following-sibling::android.widget.TextView')
    ADDRESS_SERVER_INPUT = (By.CLASS_NAME, 'android.widget.EditText')

    PORT_SERVER_FIELD = (By.XPATH, '//android.widget.TextView[@text="Порт сервера:"]/following-sibling::android.widget.TextView')
    PORT_SERVER_INPUT = (By.CLASS_NAME, 'android.widget.EditText')

    SAVE_BUTTON = by_text("СОХРАНИТЬ")
    CLOSE_BUTTON = by_text("ОТМЕНИТЬ")

    @shared_step("Проверить наличие всех элементов на странице настроек")
    def verify_all_settings_elements_present(self, device_id=None):
        elements = [
            ("Кнопка «Проверка связи»", by_text("ПРОВЕРКА СВЯЗИ")),
            ("Кнопка «Список исправлений по версиям»", by_desc("СПИСОК ИСПРАВЛЕНИЙ ПО ВЕРСИЯМ")),
            ("Кнопка «Изменить стартовую страницу»", by_text("ИЗМЕНИТЬ СТАРТОВУЮ СТРАНИЦУ")),
            ("Адрес сервера", by_text("Адрес сервера:")),
            ("Порт сервера", by_text("Порт сервера:")),
            ("Порт сервиса печати", by_text("Порт сервиса печати:")),
            ("Переключатель «Использовать камеру для сканирования»", by_text("Использовать камеру для сканирования")),
            ("Переключатель «Автоматическое считывание через камеру»", by_text("Автоматическое считывание через камеру")),
            ("Переключатель «Автоматически завершать задание»", by_text("Автоматически завершать задание")),
            ("Переключатель «Разрешить сериализацию, если статус задания готов к печати или идёт печать»", by_text("Разрешить сериализацию, если статус задания готов к печати или идёт печать")),
            ("Переключатель «Контролировать печать агрегата»", by_text("Контролировать печать агрегата")),
            ("Переключатель «Режим работы с отсканированными кодами»", by_text("Режим работы c отсканированными кодами")),
            ("Переключатель «Контроль изменений при быстрой агрегации»", by_text("Контроль изменений при быстром изменении агрегата")),
            ("Переключатель «Разрешить изменять агрегат введенных в оборот и нанесенных (не для быстрого)»", by_text("Разрешить изменять агрегат введённых в оборот и нанесённых (не для быстрого)")),
            ("Разрешить типографские коды агрегата", by_text("Разрешить типографские коды агрегата")),
            ("Отображать поле ввода веса поддона", by_text("Отображать поле ввода веса поддона")),
            ("Переключатель «Контролировать печать наборов»", by_text("Контролировать печать наборов")),
            ("ezpl", by_desc("ezpl")),
            ("tspl", by_desc("tspl")),
            ("zpl", by_text("zpl")),
            ("Использовать свободный шаблон при агрегировании", by_text("Использовать свободный шаблон при агрегирование")),
            ("Использовать свободный принтер при агрегировании", by_text("Использовать свободный принтер при агрегирование")),
            ("Переключатель «Режим отладки»", by_text("Режим отладки")),
            ("Переключатель «Увеличить шрифт»", by_text("Увеличить шрифт")),
            ("Переключатель «Обмен с 1С»", by_text("Обмен с 1С")),
            ("Кнопка «Инструкция по настройке ТСД»", by_text("Инструкция по настройке ТСД")),
            ("Кнопка «Тема приложения»", by_text("Тема приложения")),
        ]

        if device_id is not None:
            id_text = f"ID устройства - {device_id}"
            elements.insert(3, ("ID устройства", by_text(id_text)))

        for name, locator in elements:
            if not self.is_displayed(locator, timeout=1):
                self.scroll_to_element(locator, max_swipes=2)
                if not self.is_displayed(locator, timeout=1):
                    raise AssertionError(f"Элемент '{name}' не найден на странице настроек после прокрутки")

        self.swipe_up(0.1)
        self.scroll_to_element_up(self.CHECK_CONNECTION_BUTTON)

    @shared_step("Нажать 'ПРОВЕРКА СВЯЗИ'")
    def tap_check_connection_button(self):
        self.scroll_to_element_up(self.CHECK_CONNECTION_BUTTON)
        self.tap(self.CHECK_CONNECTION_BUTTON)

    @shared_step("Проверить, что появилось сообщение об успешном подключении")
    def success_check_connection_is_displayed(self):
        assert self.is_displayed(self.SUCCESSFUL_CHECK_CONNECTION), "Сообщение об успешном подключении не найдено"
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="success_connection_message",
            attachment_type=allure.attachment_type.PNG
        )
        self.tap(self.SUCCESSFUL_CHECK_CONNECTION)

    @shared_step("Проверить, что появилось сообщение об ошибке подключения")
    def unsuccess_check_connection_is_displayed(self, timeout=20):
        assert self.is_displayed(self.UNSUCCESSFUL_CHECK_CONNECTION, timeout=timeout), \
            "Сообщение об ошибке подключения не найдено"
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="unsuccess_connection_message",
            attachment_type=allure.attachment_type.PNG
        )
        self.tap(self.UNSUCCESSFUL_CHECK_CONNECTION)

    @shared_step("Нажать 'СПИСОК ИСПРАВЛЕНИЙ ПО ВЕРСИЯМ'")
    def tap_list_fixes_version_button(self):
        self.tap(self.LIST_FIXES_VERSION_BUTTON)

    @shared_step("Проверить список исправлений по версиям")
    def verify_all_versions(self, versions: dict):
        for version, details in versions.items():
            header = by_desc(version)
            # значение — текст деталей; для особых случаев можно передать готовый локатор
            details_locator = details if isinstance(details, tuple) else by_text(details)

            self.scroll_to_element(header)
            self.tap(header)

            if not self.is_displayed(details_locator, timeout=1):
                self.scroll_to_element(details_locator)

            assert self.is_displayed(details_locator, timeout=1), \
                f"Детали для версии '{version}' не отображаются после раскрытия и свайпа!"

    @shared_step("Получить отображаемую версию приложения")
    def get_displayed_version(self) -> str:
        version_element = self.find_element(self.VERSION_TEXT)
        full_text = version_element.text
        import re
        match = re.search(r'(\d+)$', full_text)
        if match:
            return match.group()
        raise ValueError(f"Не удалось извлечь версию из текста: {full_text}")

    @shared_step("Сохранить настройки (нажать СОХРАНИТЬ)")
    def tap_save_button(self):
        self.tap(self.SAVE_BUTTON)

    @shared_step("Сохранить настройки (нажать ОТМЕНИТЬ)")
    def tap_close_button(self):
        self.tap(self.CLOSE_BUTTON)

    @shared_step("Получить текущий отображаемый адрес сервера")
    def get_current_address_server(self):
        return self.get_text(self.ADDRESS_SERVER_FIELD)

    @shared_step("Нажать на поле 'Адрес сервера'")
    def tap_address_server_field(self):
        self.tap(self.ADDRESS_SERVER_FIELD)

    @shared_step("Нажать на поле 'Адрес сервера' и проверить элементы редактирования")
    def open_address_edit_and_check_elements(self):
        self.tap(self.ADDRESS_SERVER_FIELD)
        assert self.is_displayed(self.ADDRESS_SERVER_INPUT), \
            "Поле 'Адрес сервера' не отображается после тапа"
        assert self.is_displayed(self.SAVE_BUTTON), \
            "Кнопка 'СОХРАНИТЬ' не отображается после тапа"
        assert self.is_displayed(self.CLOSE_BUTTON), \
            "Кнопка 'ОТМЕНИТЬ' не отображается после тапа"

    @shared_step("Ввести адрес сервера: {address}")
    def input_address(self, address):
        self.input_text(self.ADDRESS_SERVER_INPUT, address)

    @shared_step("Ввести адрес '{address}' и сохранить")
    def enter_address_and_save(self, address):
        self.tap_address_server_field()
        self.input_address(address)
        self.tap_save_button()

    @shared_step("Проверить, что адрес сервера равен {expected_address}")
    def assert_address_server_equals(self, expected_address):
        actual = self.get_current_address_server()
        assert actual == expected_address, f"Ожидался адрес {expected_address}, получен {actual}"
        allure.attach(self.driver.get_screenshot_as_png(), name=f"address_{expected_address}", attachment_type=allure.attachment_type.PNG)

    @shared_step("Нажать на поле 'Порт сервера'")
    def tap_port_server_field(self):
        self.tap(self.PORT_SERVER_FIELD)

    @shared_step("Ввести порт: {port}")
    def input_port(self, port):
        self.input_text(self.PORT_SERVER_INPUT, port)

    @shared_step("Ввести порт '{port}' и сохранить")
    def enter_port_and_save(self, port):
        self.tap_port_server_field()
        self.input_port(port)
        self.tap_save_button()

    @shared_step("Получить текущий отображаемый порт сервера")
    def get_current_port_server(self):
        return self.get_text(self.PORT_SERVER_FIELD)

    def ensure_port_is(self, expected_port: str):
        with shared_step(f"Проверить порт сервера: {expected_port}"):
            current_port = self.get_current_port_server().strip()
            if current_port == expected_port:
                return
            self.tap_port_server_field()
            self.input_port(expected_port)
            self.tap_save_button()

