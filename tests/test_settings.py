# test_settings.py

import pytest
import allure
from utils.adb_utils import AdbUtils


@pytest.mark.smoke
@allure.feature("Настройки")
class TestSettings:
    @allure.title("DMC Mobile. Настройки. Проверка связи.")
    def test_check_connection(self, settings_page):
        with allure.step("Ввод неверного адреса и порта"):
            settings_page.swipe_down(0.4)
            settings_page.enter_address_and_save("0.0.0.0")
            settings_page.enter_port_and_save("0000")

        with allure.step("Проверка связи с неверными данными"):
            settings_page.swipe_up(0.4)
            settings_page.tap_check_connection_button()
            settings_page.unsuccess_check_connection_is_displayed()

        with allure.step("Ввод корректного адреса и порта"):
            settings_page.swipe_down(0.4)
            settings_page.enter_address_and_save("10.76.10.102")
            settings_page.enter_port_and_save("8125")

        with allure.step("Проверка связи с корректными данными"):
            settings_page.swipe_up(0.4)
            settings_page.tap_check_connection_button()
            settings_page.success_check_connection_is_displayed()

    @allure.title("DMC Mobile. Настройки. Список исправлений по версиям")
    def test_list_fixes_version(self, settings_page):
        with allure.step("Проверка списа исправленных версий"):
            settings_page.tap_list_fixes_version_button()
            settings_page.verify_all_versions()

    @allure.title("DMC Mobile. Настройки. Проверка версии приложения")
    def test_app_version_matches_displayed(self, settings_page):
        displayed_version = settings_page.get_displayed_version()

        package = "com.dmc_mobile"
        actual_version = AdbUtils.get_app_version_from_adb(package)

        with allure.step(f"Сравнить версии: отображаемая={displayed_version}, реальная={actual_version}"):
            assert displayed_version == actual_version, \
                f"Версия в приложении ({displayed_version}) не совпадает с реальной версией APK ({actual_version})"

    @allure.title("DMC Mobile. Настройки. Адрес сервера. Проверка редактирования")
    def test_address_server_editing_check(self, settings_page):
        with allure.step("Ввод корректного адреса и порта"):
            settings_page.swipe_down(0.4)
            settings_page.enter_address_and_save("10.76.10.102")
            settings_page.enter_port_and_save("8125")

        with allure.step("Проверить адрес сервера"):
            default_address = "10.76.10.102"
            settings_page.assert_address_server_equals(default_address)

        with allure.step("Открыть изменения адреса и нажать 'Отменить'"):
            settings_page.tap_address_server_field()
            settings_page.tap_close_button()

        with allure.step("Изменить адрес на 10.76.10.101 и сохранить"):
            new_address = "10.76.10.101"
            settings_page.enter_address_and_save(new_address)

        with allure.step("Проверить, что связь с сервером потеряна"):
            settings_page.swipe_up(0.4)
            settings_page.tap_check_connection_button()
            settings_page.unsuccess_check_connection_is_displayed()

        with allure.step("Вернуть адрес 10.76.10.102 и сохранить"):
            settings_page.swipe_down(0.4)
            original_address = "10.76.10.102"
            settings_page.enter_address_and_save(original_address)

        with allure.step("Проверить, что связь с сервером восстановлена"):
            settings_page.swipe_up(0.2)
            settings_page.tap_check_connection_button()
            settings_page.success_check_connection_is_displayed()
