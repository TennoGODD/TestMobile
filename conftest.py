#conftest.py

import json
import os

import allure
import testit
import pytest
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from config.config import Config
from pages.serialization_page import SerializationPage
from pages.settings_page import SettingsPage
from pages.code_information_page import CodeInformationPage
from utils.step_utils import shared_step
from utils.db_client import DatabaseClient
from utils.api_client import DmcApiClient
from utils.printer_emulator import PrinterEmulator
from utils.adb_utils import AdbUtils
from test_data.products import WATER, LINE


# Задания, созданные заранее (на этапе сборки) для тестов с маркером @pytest.mark.task.
# Ключ — node id теста, значение — taskid или ошибка создания.
_precreated_tasks = {}
_precreate_errors = {}


# Категории для вкладки Categories в Allure — группируют падения по типу.
# messageRegex матчится по (уже укороченному) сообщению об ошибке.
ALLURE_CATEGORIES = [
    {
        "name": "Проблема с подключением к серверу",
        "matchedStatuses": ["failed", "broken"],
        "messageRegex": ".*(подключени|сервер|соединени).*",
    },
    {
        "name": "Элемент не найден на экране",
        "matchedStatuses": ["broken", "failed"],
        "messageRegex": ".*(не найден|не отображается|NoSuchElement|TimeoutException).*",
    },
    {
        "name": "Ошибка REST API DMC",
        "matchedStatuses": ["failed", "broken"],
        "messageRegex": ".*(DmcApiError|API DMC).*",
    },
    {
        "name": "Ошибка базы данных",
        "matchedStatuses": ["failed", "broken"],
        "messageRegex": ".*(psycopg2|taskid|агрегат уровня).*",
    },
    {
        "name": "Несовпадение данных на экране",
        "matchedStatuses": ["failed"],
        "messageRegex": ".*(ожидал|Ожидал|успешно отсканирован|Верифицировано).*",
    },
]


def _write_allure_metadata(alluredir):
    """Кладёт в папку результатов файлы, из которых Allure строит блоки
    Environment, Categories на Overview."""
    os.makedirs(alluredir, exist_ok=True)

    with open(os.path.join(alluredir, "categories.json"), "w", encoding="utf-8") as f:
        json.dump(ALLURE_CATEGORIES, f, ensure_ascii=False, indent=2)

    env = {
        "Platform": "Android",
        "Device.UDID": Config.UDID,
        "App.Package": Config.MOBILE_PACKAGE,
        "Server": f"{Config.SERVER_ADDRESS}:{Config.SERVER_PORT}",
        "Appium": f"{Config.APPHOST}:{Config.APPPORT}",
    }
    try:
        env["App.Version"] = AdbUtils.get_app_version_from_adb(Config.MOBILE_PACKAGE, udid=Config.UDID)
    except Exception:
        pass  # adb недоступен или устройство не подключено — просто без версии

    with open(os.path.join(alluredir, "environment.properties"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"{key}={value}" for key, value in env.items()))


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "task(amount, aggr_ids=None, gtin=None, line=None): предсоздать задание DMC для теста"
    )

    try:
        alluredir = config.getoption("--alluredir")
    except (ValueError, KeyError):
        alluredir = None  # allure-pytest не установлен
    if alluredir:
        _write_allure_metadata(alluredir)


def pytest_collection_modifyitems(config, items):
    """Заранее (на этапе сборки) создаёт задания для тестов с маркером task.

    Создаются только реально собранные тесты (с учётом -k/-m), поэтому лишних
    заданий не будет. Пока идут первые тесты, эти задания дозревают до статуса
    «готово» параллельно — фикстура task потом почти не ждёт.
    """
    if config.getoption("--collect-only"):
        return  # при сборке без запуска не трогаем API

    marked = [(item, item.get_closest_marker("task")) for item in items]
    marked = [(item, marker) for item, marker in marked if marker is not None]
    if not marked:
        return

    api = DmcApiClient(Config.API_URL)
    try:
        for item, marker in marked:
            gtin = marker.kwargs.get("gtin", WATER.gtin)
            line = marker.kwargs.get("line", LINE)
            amount = marker.kwargs["amount"]
            aggr_ids = marker.kwargs.get("aggr_ids")
            try:
                _precreated_tasks[item.nodeid] = api.create_task_by_spec(
                    gtin=gtin, line=line, amount=amount, aggr_ids=aggr_ids
                )
            except Exception as exc:
                # не роняем всю сборку из-за одного задания — тест упадёт понятно
                _precreate_errors[item.nodeid] = exc
    finally:
        api.close()


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

@pytest.fixture(scope="session")
def db():
    db_client = DatabaseClient(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )
    yield db_client
    db_client.close()

@pytest.fixture(scope="session")
def api():
    client = DmcApiClient(Config.API_URL)
    yield client
    client.close()

@pytest.fixture(autouse=True)
def _testit_allure_link():
    """Прикрепляет к каждому автотесту в TestIT ссылку на Allure-отчёт (GitHub Pages)."""
    testit.addLink(
        url=Config.ALLURE_REPORT_URL,
        title="Allure-отчёт (GitHub Pages)",
        type="Related",
    )
    yield

@pytest.fixture
def task(request, db):
    """Отдаёт taskid задания, созданного заранее по маркеру @pytest.mark.task,
    и дожидается его готовности (обычно оно уже дозрело за время прошлых тестов)."""
    nodeid = request.node.nodeid
    if nodeid in _precreate_errors:
        pytest.fail(f"Не удалось создать задание для теста: {_precreate_errors[nodeid]}")
    taskid = _precreated_tasks.get(nodeid)
    if taskid is None:
        pytest.fail("Для теста нет предсозданного задания — добавьте маркер @pytest.mark.task(...)")
    db.wait_for_task_status(taskid, target_status=6, timeout=400)
    return taskid

@pytest.fixture
def printer_kigu():
    emulator = PrinterEmulator(host=Config.PRINTER_HOST, port=Config.PRINTER_PORT_KIGU)
    emulator.start()
    yield emulator
    emulator.stop()

@pytest.fixture
def printer_kitu():
    emulator = PrinterEmulator(host=Config.PRINTER_HOST, port=Config.PRINTER_PORT_KITU)
    emulator.start()
    yield emulator
    emulator.stop()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def _short_error(excinfo) -> str:
    """Короткое сообщение о падении вместо простыни.

    У ошибок Selenium/Appium в str(exception) вшит java-стектрейс
    UiAutomator2-сервера — отрезаем его, но добавляем файл и строку
    в коде проекта, где произошло падение.
    """
    message = str(excinfo.value).split("Stacktrace:", 1)[0]
    if message.startswith("Message: "):
        message = message[len("Message: "):]
    message = message.strip()

    place = ""
    try:
        for entry in reversed(excinfo.traceback):
            path = str(entry.path)
            if path.startswith(ROOT_DIR) and ".venv" not in path:
                place = f" ({os.path.relpath(path, ROOT_DIR)}:{entry.lineno + 1})"
                break
    except Exception:
        pass

    return f"{excinfo.typename}: {message}{place}"


def _trim_webdriver_exception(exc):
    """Убирает громоздкий java-стектрейс UiAutomator2 из selenium/appium-
    исключений, чтобы короткое сообщение попало в Allure, TestIT и терминал.

    Java-трейс лежит в атрибуте .stacktrace (его подклеивает __str__), а сам
    текст ошибки — в .msg. Достаточно обнулить .stacktrace и подрезать .msg.
    """
    if getattr(exc, "stacktrace", None):
        try:
            exc.stacktrace = None
        except Exception:
            pass
    msg = getattr(exc, "msg", None)
    if isinstance(msg, str) and "Stacktrace:" in msg:
        try:
            exc.msg = msg.split("Stacktrace:", 1)[0].strip()
        except Exception:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Укорачиваем исключение ДО yield — чтобы Allure/TestIT, которые читают
    # call.excinfo.value внутри, увидели уже короткое сообщение.
    if call.excinfo is not None:
        _trim_webdriver_exception(call.excinfo.value)

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="screenshot_on_fail",
                attachment_type=allure.attachment_type.PNG
            )
            # is_text=True здесь означает «приложить содержимое из памяти, а не
            # путь к файлу»; байты PNG записываются как есть (см. convert_body_of_attachment).
            # Если передать (name, bytes) позиционно, bytes попадут в is_text, а имя
            # файла — в data, и в TestIT уедет текстовый файл с текстом имени.
            testit.addAttachments(screenshot, is_text=True, name="screenshot_on_fail.png")

        excinfo = call.excinfo
        if excinfo:
            report.longrepr = _short_error(excinfo)

def _open_section(driver, page_class):
    """Открывает раздел приложения через меню и возвращает его page object.
    Страница описывает себя сама: MENU_BUTTON, PAGE_TITLE и SECTION_NAME
    заданы атрибутами класса (см. BasePage).
    """
    page = page_class(driver)

    with shared_step(f'Открытие раздела "{page_class.SECTION_NAME}"'):
        page.tap_warning_if_present()

        for attempt in (1, 2):
            try:
                page.tap_content_button()
                page.wait.until(EC.element_to_be_clickable(page_class.MENU_BUTTON))
                page.tap(page_class.MENU_BUTTON)
                page.wait.until(EC.visibility_of_element_located(page_class.PAGE_TITLE))
                break
            except Exception:
                if attempt == 2:
                    raise
                page.tap_warning_if_present()

        page.tap_warning_if_present()

    return page

@pytest.fixture
def settings_page(driver):
    with shared_step("Открытие раздела 'Настройки'"):
        return _open_section(driver, SettingsPage)

@pytest.fixture
def code_information_page(driver):
    with shared_step("Открытие раздела 'Информация по коду'"):
        return _open_section(driver, CodeInformationPage)

@pytest.fixture
def serialization_page(driver):
    with shared_step("Открытие раздела 'Сериализация'"):
        return _open_section(driver, SerializationPage)
