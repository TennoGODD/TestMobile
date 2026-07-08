# test_settings.py

from utils.step_utils import shared_step, shared_title
import allure
import testit
from config.config import Config
from utils.adb_utils import AdbUtils
from test_data.versions import VERSION_FIXES


@allure.feature("Настройки")
@allure.severity(allure.severity_level.NORMAL)
@testit.labels("settings")
class TestSettings:
    @shared_title("DMC Mobile. Настройки. Проверка связи.")
    @testit.externalId("71")
    def test_check_connection(self, settings_page):
        with shared_step("Открытие раздела 'Настройки' и проверка наличия всех элементов"):
            settings_page.verify_all_settings_elements_present(device_id=Config.DEVICE_ID)

        with shared_step("Проверка связи с неверными данными"):
            with shared_step("Ввод неверного адреса и порта"):
                settings_page.swipe_down(0.4)
                settings_page.enter_address_and_save("0.0.0.0")
                settings_page.enter_port_and_save("0000")

            with shared_step("Нажать кнопку 'Проверить связь' и убедиться, что связь не установлена"):
                settings_page.swipe_up(0.1)
                settings_page.tap_check_connection_button()
                settings_page.unsuccess_check_connection_is_displayed()

        with shared_step("Проверка связи с корректными данными"):
            with shared_step("Ввод корректного адреса и порта"):
                settings_page.swipe_down(0.4)
                settings_page.enter_address_and_save(Config.SERVER_ADDRESS)
                settings_page.enter_port_and_save(Config.SERVER_PORT)

            with shared_step("Нажать кнопку 'Проверить связь' и убедиться, что связь установлена"):
                settings_page.swipe_up(0.1)
                settings_page.tap_check_connection_button()
                settings_page.success_check_connection_is_displayed()

    @shared_title("DMC Mobile. Настройки. Проверка версии приложения")
    @testit.externalId("73")
    def test_app_version_matches_displayed(self, settings_page):
        displayed_version = settings_page.get_displayed_version()
        actual_version = AdbUtils.get_app_version_from_adb(Config.MOBILE_PACKAGE, udid=Config.UDID)

        with allure.step(f"Сравнить версии: отображаемая={displayed_version}, реальная={actual_version}"):
            assert displayed_version == actual_version, \
                f"Версия в приложении ({displayed_version}) не совпадает с реальной версией APK ({actual_version})"

    @shared_title("DMC Mobile. Настройки. Адрес сервера. Проверка редактирования")
    @testit.externalId("491")
    def test_address_server_editing_check(self, settings_page):

            
        with shared_step("Нажать на значение адреса тестового сервера"):

            settings_page.swipe_down(0.4)
            settings_page.ensure_port_is(Config.SERVER_PORT)
            settings_page.swipe_up(0.1)

            settings_page.swipe_down(0.4)
            settings_page.open_address_edit_and_check_elements()

        with shared_step("Нажать кнопку 'Отменить'"):
            settings_page.tap_close_button()

        wrong_address = "10.76.10.101"  
        
        with shared_step(f"Изменить адрес на {wrong_address} и сохранить"):
            settings_page.enter_address_and_save(wrong_address)
            assert settings_page.get_current_address_server() == wrong_address

        with shared_step("Проверить, что связь с сервером потеряна"):
            settings_page.swipe_up(0.1)
            settings_page.tap_check_connection_button()
            settings_page.unsuccess_check_connection_is_displayed()

        with shared_step(f"Вернуть адрес {Config.SERVER_ADDRESS} и сохранить"):
            settings_page.swipe_down(0.4)
            settings_page.enter_address_and_save(Config.SERVER_ADDRESS)
            assert settings_page.get_current_address_server() == Config.SERVER_ADDRESS

        with shared_step("Проверить, что связь с сервером восстановлена"):
            settings_page.swipe_up(0.1)
            settings_page.tap_check_connection_button()
            settings_page.success_check_connection_is_displayed()

    @shared_title("DMC Mobile. Настройки. Список исправлений по версиям")
    @testit.externalId("72")
    def test_list_fixes_version(self, settings_page):
        with shared_step("Нажать кнопку 'Список исправлений по версиям'"):
            settings_page.tap_list_fixes_version_button()
        with shared_step("Развернуть список исправлений по очереди для каждой версии"):    
            settings_page.verify_all_versions(VERSION_FIXES)
