#config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APPHOST = "127.0.0.1"
    APPPORT ="4808"
    UDID = "4929312"

    MOBILE_PACKAGE = "com.dmc_mobile"
    MOBILE_ACTIVITY = ".MainActivity"