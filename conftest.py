#conftest.py

import allure
import testit
import pytest
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy as By
from appium.options.android import UiAutomator2Options
from config.config import Config
from pages.content_page import ContentPage
from pages.settings_page import SettingsPage
from pages.code_information_page import CodeInformationPage



@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.udid = Config.UDID
    options.automation_name = "UiAutomator2"
    options.app_package = Config.MOBILE_PACKAGE
    options.app_activity = Config.MOBILE_ACTIVITY
    options.no_reset = True

    driver = webdriver.Remote(f"http://{Config.APPHOST}:{Config.APPPORT}/wd/hub", options=options)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_fail",
                attachment_type=allure.attachment_type.PNG
            )
            testit.addAttachments("screenshot_on_fail.png", driver.get_screenshot_as_png())

        excinfo = call.excinfo
        if excinfo:
            report.longrepr = f"{excinfo.typename}: {excinfo.value}"

@pytest.fixture
def settings_page(driver):
    wait = WebDriverWait(driver, 15)
    settings = SettingsPage(driver)
    content = ContentPage(driver)

    settings_btn = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Настройки")')
    settings_title = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Настройки подключения")')

    settings.tap_warning_if_present()
    settings.tap_content_button()

    try:
        wait.until(EC.element_to_be_clickable(settings_btn))
    except Exception:
        settings.tap_warning_if_present()
        settings.tap_content_button()
        wait.until(EC.element_to_be_clickable(settings_btn))

    content.tap_settings_button()

    try:
        wait.until(EC.visibility_of_element_located(settings_title))
    except Exception:
        settings.tap_warning_if_present()
        settings.tap_content_button()
        wait.until(EC.element_to_be_clickable(settings_btn))
        content.tap_settings_button()
        wait.until(EC.visibility_of_element_located(settings_title))

    settings.tap_warning_if_present()

    with allure.step('Открытие раздела "Настройки"'):
        return settings

@pytest.fixture
def code_information_page(driver):
    wait = WebDriverWait(driver, 15)
    code_information = CodeInformationPage(driver)
    content = ContentPage(driver)

    code_information_text = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Отсканируйте, код маркировки для получения информации по нему")')
    code_information_button = (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Информация по коду")')

    code_information.tap_warning_if_present()
    code_information.tap_content_button()

    try:
        wait.until(EC.element_to_be_clickable(code_information_button))
    except Exception:
        code_information.tap_warning_if_present()
        code_information.tap_content_button()
        wait.until(EC.element_to_be_clickable(code_information_button))

    content.tap_code_information_button()

    try:
        wait.until(EC.visibility_of_element_located(code_information_text))
    except Exception:
        code_information.tap_warning_if_present()
        code_information.tap_content_button()
        wait.until(EC.element_to_be_clickable(code_information_button))
        content.tap_settings_button()
        wait.until(EC.visibility_of_element_located(code_information_text))

    code_information.tap_warning_if_present()

    with allure.step('Открытие раздела "Информация по коду"'):
        return code_information