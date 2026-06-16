#config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APPHOST = os.getenv("APPIUM_HOST", "127.0.0.1")
    APPPORT = os.getenv("APPIUM_PORT", "4808")
    UDID = os.getenv("DEVICE_UDID", "4929312")

    MOBILE_PACKAGE = "com.dmc_mobile"
    MOBILE_ACTIVITY = ".MainActivity"