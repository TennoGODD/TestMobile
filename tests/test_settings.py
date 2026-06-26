# test_settings.py

import pytest
import testit
import allure
from utils.adb_utils import AdbUtils


@pytest.mark.smoke
@allure.feature("Настройки")
class TestSettings:
    @allure.title("DMC Mobile. Настройки. Проверка связи.")
    @testit.workItemIds("71")
    @testit.externalId("71")
    @testit.displayName("DMC Mobile. Настройки. Проверка связи.")
    def test_check_connection(self, settings_page):

        settings_page.verify_all_settings_elements_present(device_id="301f48cb08545652")

        with allure.step("Ввод неверного адреса и порта"):
            settings_page.swipe_down(0.4)
            settings_page.enter_address_and_save("0.0.0.0")
            settings_page.enter_port_and_save("0000")

        with allure.step("Проверка связи с неверными данными"):
            settings_page.swipe_up(0.1)
            settings_page.tap_check_connection_button()
            settings_page.unsuccess_check_connection_is_displayed()

        with allure.step("Ввод корректного адреса и порта"):
            settings_page.swipe_down(0.4)
            settings_page.enter_address_and_save("10.76.10.102")
            settings_page.enter_port_and_save("8125")

        with allure.step("Проверка связи с корректными данными"):
            settings_page.swipe_up(0.1)
            settings_page.tap_check_connection_button()
            settings_page.success_check_connection_is_displayed()

    @allure.title("DMC Mobile. Настройки. Проверка версии приложения")
    @testit.workItemIds("73")
    @testit.externalId("73")
    @testit.displayName("DMC Mobile. Настройки. Проверка версии приложения")
    def test_app_version_matches_displayed(self, settings_page):
        displayed_version = settings_page.get_displayed_version()

        package = "com.dmc_mobile"
        actual_version = AdbUtils.get_app_version_from_adb(package)

        with allure.step(f"Сравнить версии: отображаемая={displayed_version}, реальная={actual_version}"):
            assert displayed_version == actual_version, \
                f"Версия в приложении ({displayed_version}) не совпадает с реальной версией APK ({actual_version})"

    @allure.title("DMC Mobile. Настройки. Адрес сервера. Проверка редактирования")
    @testit.workItemIds("491")
    @testit.externalId("491")
    @testit.displayName("DMC Mobile. Настройки. Адрес сервера. Проверка редактирования")
    def test_address_server_editing_check(self, settings_page):
        with allure.step("Убедиться, что порт корректен"):
            settings_page.swipe_down(0.4)
            settings_page.ensure_port_is("8125")
            settings_page.swipe_up(0.1)

        with allure.step("Открыть изменения адреса и нажать 'Отменить'"):
            settings_page.swipe_down(0.4)
            settings_page.open_address_edit_and_check_elements()
            settings_page.tap_close_button()

        with allure.step("Изменить адрес на 10.76.10.101 и сохранить"):
            new_address = "10.76.10.101"
            settings_page.enter_address_and_save(new_address)
            assert settings_page.get_current_address_server() == new_address

        with allure.step("Проверить, что связь с сервером потеряна"):
            settings_page.swipe_up(0.1)
            settings_page.tap_check_connection_button()
            settings_page.unsuccess_check_connection_is_displayed()

        with allure.step("Вернуть адрес 10.76.10.102 и сохранить"):
            settings_page.swipe_down(0.4)
            original_address = "10.76.10.102"
            settings_page.enter_address_and_save(original_address)
            assert settings_page.get_current_address_server() == original_address

        with allure.step("Проверить, что связь с сервером восстановлена"):
            settings_page.swipe_up(0.1)
            settings_page.tap_check_connection_button()
            settings_page.success_check_connection_is_displayed()

    @allure.title("DMC Mobile. Настройки. Список исправлений по версиям")
    @testit.workItemIds("72")
    @testit.externalId("72")
    @testit.displayName("DMC Mobile. Настройки. Список исправлений по версиям")
    def test_list_fixes_version(self, settings_page):
        with allure.step("Проверка списа исправленных версий"):
            settings_page.tap_list_fixes_version_button()
            settings_page.verify_all_versions()
