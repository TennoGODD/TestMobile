#config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APPHOST = os.getenv("APPIUM_HOST", "127.0.0.1")
    APPPORT = os.getenv("APPIUM_PORT", "4808")
    UDID = os.getenv("UDID", "4929312")
    DEVICE_ID = os.getenv("DEVICE_ID", "301f48cb08545652")  # ID устройства на странице настроек

    DB_HOST = os.getenv("DB_HOST", "10.76.10.102")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "wip_1047")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    # адрес и порт сервера DMC, которые вводятся в настройках приложения
    SERVER_ADDRESS = os.getenv("DMC_SERVER_ADDRESS", "10.76.10.102")
    SERVER_PORT = os.getenv("DMC_SERVER_PORT", "8025")

    # REST API DMC (создание заданий) — тот же сервер, что и в настройках приложения
    API_URL = os.getenv("DMC_API_URL", f"http://{SERVER_ADDRESS}:{SERVER_PORT}")

    # Эмуляторы принтера — на них приложение шлёт задания печати агрегатов
    # (порты сервиса печати в настройках ТСД должны указывать на машину с тестами)
    PRINTER_HOST = os.getenv("PRINTER_HOST", "0.0.0.0")
    PRINTER_PORT_KIGU = int(os.getenv("PRINTER_PORT_KIGU", "9102"))  # агрегат 0 уровня (КИГУ)
    PRINTER_PORT_KITU = int(os.getenv("PRINTER_PORT_KITU", "9103"))  # агрегат 1 уровня (КИТУ)

    MOBILE_PACKAGE = "com.dmc_mobile"
    MOBILE_ACTIVITY = ".MainActivity"

    # Allure-отчёт на GitHub Pages — ссылку на него прикрепляем к тестам в TestIT
    ALLURE_REPORT_URL = os.getenv("ALLURE_REPORT_URL", "https://tennogodd.github.io/TestMobile/")
