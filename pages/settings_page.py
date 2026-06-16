# settings_page.py

import allure
from base.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as By


class SettingsPage(BasePage):
    CONTENT_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(2)')

    SETTINGS_TITLE = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Настройки")')

    WARNING_FIELD_1 = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Введите адрес сервера, для продложения работы")')
    WARNING_FIELD_2 = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Внимание! Не удалось подключиться к серверу!")')

    CHECK_CONNECTION_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ПРОВЕРКА СВЯЗИ")')
    SUCCESSFUL_CHECK_CONNECTION = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Успешное подключение к серверу!")')
    UNSUCCESSFUL_CHECK_CONNECTION = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Ошибка! Подключение к серверу отсутвует!")')

    LIST_FIXES_VERSION_BUTTON = (By.ACCESSIBILITY_ID, "СПИСОК ИСПРАВЛЕНИЙ ПО ВЕРСИЯМ")
    VERSION_ITEMS = {
        "1, 20.05.25": {
            "header": (By.ACCESSIBILITY_ID, "1, 20.05.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена работа с наборами")'),
        },
        "2, 29.05.25": {
            "header": (By.ACCESSIBILITY_ID, "2, 29.05.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлены переменные weight_04 и weight_05")'),
        },
        "3, 18.06.25": {
            "header": (By.ACCESSIBILITY_ID, "3, 18.06.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Добавлено:")'),
        },
        "4, 25.06.25": {
            "header": (By.ACCESSIBILITY_ID, "4, 25.06.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- В быстрое изменение агрегата добавлена возможность игнорировать задание")'),
        },
        "5, 03.07.25": {
            "header": (By.ACCESSIBILITY_ID, "5, 03.07.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Исправлена ошибка при работе с типографскими кодами. Когда в БД записывался неправильно криптохвост")'),
        },
        "6, 07.07.25": {
            "header": (By.ACCESSIBILITY_ID, "6, 07.07.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Исправлена ошибка при работе с 4х значными типографскими кодами. Когда в БД записывался неправильно криптохвост")'),
        },
        "7, 21.07.25": {
            "header": (By.ACCESSIBILITY_ID, "7, 21.07.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Исправлена ошибка при работе с переменной slifetime")'),
        },
        "10, 23.07.25": {
            "header": (By.ACCESSIBILITY_ID, "10, 23.07.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена работа с белорусскими кодами агрегата")'),
        },
        "11, 23.07.25": {
            "header": (By.ACCESSIBILITY_ID, "11, 23.07.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена возможность агрегировать 0 и 1 уровень одновременно вовремя сериализации. Теперь в тот момент, когда вы берёте задание в работу по сериализации и есть несколько уровней агрегации приложение задаст вопрос и выведет кнопки в виде списка названий нулевого и первого уровня агргегации, а так же кнопка «Нет» - что бы выполнить сериализацию без агрегирования")'),
        },
        "12, 21.08.25": {
            "header": (By.ACCESSIBILITY_ID, "12, 21.08.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Интеграция с ТСД АТОЛ Smart M20")'),
        },
        "13, 25.08.25": {
            "header": (By.ACCESSIBILITY_ID, "13, 25.08.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена обработка переменной cell")'),
        },
        "14, 05.09.25": {
            "header": (By.ACCESSIBILITY_ID, "14, 05.09.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена возможность печатать через old printer (Работает только с шаблонами из DMC (Не редактор этикеток))")'),
        },
        "15, 19.09.25": {
            "header": (By.ACCESSIBILITY_ID, "15, 19.09.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" - Убран приоритет при выборе шаблона, который находился где штучный шаблон")'),
        },
        "16, 30.09.25": {
            "header": (By.ACCESSIBILITY_ID, "16, 30.09.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Срок годности теперь сперва берётся из задания, из переменной expiration_date")'),
        },
        "17, 02.10.25": {
            "header": (By.ACCESSIBILITY_ID, "17, 02.10.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- В коде информации по коду в результате агрегации добавлено наименование продукции")'),
        },
        "18, 02.10.25": {
            "header": (By.ACCESSIBILITY_ID, "18, 02.10.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Логи переехали в Download/dmc/logs/")'),
        },
        "19, 10.10.25": {
            "header": (By.ACCESSIBILITY_ID, "19, 10.10.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- В документ логирования теперь записываются последние 10 запросов")'),
        },
        "20, 29.10.25": {
            "header": (By.ACCESSIBILITY_ID, "20, 29.10.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Приложение обновилось на новую платформу, что уменьшает размер apk-файла")'),
        },
        "20.5, 10.11.25": {
            "header": (By.ACCESSIBILITY_ID, "20.5, 10.11.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена переменная pack_ean13barcode")'),
        },
        "20.7, 19.11.25": {
            "header": (By.ACCESSIBILITY_ID, "20.7, 19.11.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена проверка-поиск штучного кода в агрегатах")'),
        },
        "20.76, 09.12.25": {
            "header": (By.ACCESSIBILITY_ID, "20.76, 09.12.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлено обработка условий в переменных").instance(0)'),
        },
        "20.8, 16.12.25": {
            "header": (By.ACCESSIBILITY_ID, "20.8, 16.12.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Добавлена настройка выбора языка принтера, для oldprinter ")'),
        },
        "20.10, 19.12.25": {
            "header": (By.ACCESSIBILITY_ID, "20.10, 19.12.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- При отбраковке весового агрегата теперь вычисляется вес, в задание и родителе ")'),
        },
        "20.11, 25.12.25": {
            "header": (By.ACCESSIBILITY_ID, "20.11, 25.12.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Исправлено, когда в версиях с 20.7.7 при повторе печати принтер брался из линии, а не ранее выбранный незанятый принтер")'),
        },
        "20.12, 30.12.25": {
            "header": (By.ACCESSIBILITY_ID, "20.12, 30.12.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Исправлена ошибка, когда в быстрой агреганции могли не добавляться и изыматься коды")'),
        },
        "21, 20.01.26": {
            "header": (By.ACCESSIBILITY_ID, "21, 20.01.26"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView").instance(6)'),
        },
        "22, 30.12.25": {
            "header": (By.ACCESSIBILITY_ID, "22, 30.12.25"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- В печати вложений теперь можно выбрать язык принера")'),
        },
        "23, 30.03.26": {
            "header": (By.ACCESSIBILITY_ID, "23, 30.03.26"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- При первом запуске приложения, ip-адрес сервера установлен - 0.0.0.0 и приложение перенаправляет в настройки")'),
        },
        "23r2, 07.04.26": {
            "header": (By.ACCESSIBILITY_ID, "23r2, 07.04.26"),
            "details": (By.ANDROID_UIAUTOMATOR,
                        'new UiSelector().text("- Исправлено, когда новые версии ТСД не отображались в ЛК DMC")'),
        },
        "24, 30.04.26": {
            "header": (By.ACCESSIBILITY_ID, "24, 30.04.26"),
            "details": (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("- Исправлено когда product0 не брался, если в конце строки не было переноса")'),
        },
    }

    VERSION_TEXT = (By.XPATH, '//android.widget.TextView[@text="Версия приложения:"]/following-sibling::android.widget.TextView')

    ADDRESS_SERVER_FIELD = (By.XPATH, '//android.widget.TextView[@text="Адрес сервера:"]/following-sibling::android.widget.TextView')
    ADDRESS_SERVER_INPUT = (By.CLASS_NAME, 'android.widget.EditText')

    PORT_SERVER_FIELD = (By.XPATH, '//android.widget.TextView[@text="Порт сервера:"]/following-sibling::android.widget.TextView')
    PORT_SERVER_INPUT = (By.CLASS_NAME, 'android.widget.EditText')

    SAVE_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("СОХРАНИТЬ")')
    CLOSE_BUTTON = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ОТМЕНИТЬ")')

    @allure.step("Открыть меню разделов")
    def tap_content_button(self):
        self.tap(self.CONTENT_BUTTON)

    @allure.step("Закрыть предупреждение")
    def tap_warning_if_present(self, timeout=2):
        if self.is_displayed(self.WARNING_FIELD_1, timeout=timeout):
            self.tap(self.WARNING_FIELD_1)
        if self.is_displayed(self.WARNING_FIELD_2, timeout=timeout):
            self.tap(self.WARNING_FIELD_2)

    @allure.step("Нажать 'ПРОВЕРКА СВЯЗИ'")
    def tap_check_connection_button(self):
        self.tap(self.CHECK_CONNECTION_BUTTON)

    @allure.step("Проверить, что появилось сообщение об успешном подключении")
    def success_check_connection_is_displayed(self):
        assert self.is_displayed(self.SUCCESSFUL_CHECK_CONNECTION), "Сообщение об успешном подключении не найдено"
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="success_connection_message",
            attachment_type=allure.attachment_type.PNG
        )
        self.tap(self.SUCCESSFUL_CHECK_CONNECTION)

    @allure.step("Проверить, что появилось сообщение об ошибке подключения")
    def unsuccess_check_connection_is_displayed(self):
        assert self.is_displayed(self.UNSUCCESSFUL_CHECK_CONNECTION), "Сообщение об ошибке подключения не найдено"
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="unsuccess_connection_message",
            attachment_type=allure.attachment_type.PNG
        )
        self.tap(self.UNSUCCESSFUL_CHECK_CONNECTION)

    @allure.step("Нажать 'СПИСОК ИСПРАВЛЕНИЙ ПО ВЕРСИЯМ'")
    def tap_list_fixes_version_button(self):
        self.tap(self.LIST_FIXES_VERSION_BUTTON)

    @allure.step("Проверить список исправлений по версиям")
    def verify_all_versions(self):
        for version_key, locators in self.VERSION_ITEMS.items():
            header = locators["header"]
            details = locators["details"]

            self.scroll_to_element(header)
            self.tap(header)

            if not self.is_displayed(details, timeout=2):
                self.scroll_to_element(details)

            assert self.is_displayed(details, timeout=2), \
                f"Детали для версии '{version_key}' не отображаются после раскрытия и свайпа!"


    @allure.step("Получить отображаемую версию приложения")
    def get_displayed_version(self) -> str:
        version_element = self.find_element(self.VERSION_TEXT)
        full_text = version_element.text
        import re
        match = re.search(r'(\d+)$', full_text)
        if match:
            return match.group()
        raise ValueError(f"Не удалось извлечь версию из текста: {full_text}")

    @allure.step("Сохранить настройки (нажать СОХРАНИТЬ)")
    def tap_save_button(self):
        self.tap(self.SAVE_BUTTON)

    @allure.step("Сохранить настройки (нажать ОТМЕНИТЬ)")
    def tap_close_button(self):
        self.tap(self.CLOSE_BUTTON)

    @allure.step("Получить текущий отображаемый адрес сервера")
    def get_current_address_server(self):
        return self.get_text(self.ADDRESS_SERVER_FIELD)

    @allure.step("Нажать на поле 'Адрес сервера'")
    def tap_address_server_field(self):
        self.tap(self.ADDRESS_SERVER_FIELD)

    @allure.step("Ввести адрес сервера: {address}")
    def input_address(self, address):
        self.input_text(self.ADDRESS_SERVER_INPUT, address)

    @allure.step("Ввести адрес '{address}' и сохранить")
    def enter_address_and_save(self, address):
        self.tap_address_server_field()
        self.input_address(address)
        self.tap_save_button()

    @allure.step("Проверить, что адрес сервера равен {expected_address}")
    def assert_address_server_equals(self, expected_address):
        actual = self.get_current_address_server()
        assert actual == expected_address, f"Ожидался адрес {expected_address}, получен {actual}"
        allure.attach(self.driver.get_screenshot_as_png(), name=f"address_{expected_address}", attachment_type=allure.attachment_type.PNG)

    @allure.step("Нажать на поле 'Порт сервера'")
    def tap_port_server_field(self):
        self.tap(self.PORT_SERVER_FIELD)

    @allure.step("Ввести порт: {port}")
    def input_port(self, port):
        self.input_text(self.PORT_SERVER_INPUT, port)

    @allure.step("Ввести порт '{port}' и сохранить")
    def enter_port_and_save(self, port):
        self.tap_port_server_field()
        self.input_port(port)
        self.tap_save_button()

