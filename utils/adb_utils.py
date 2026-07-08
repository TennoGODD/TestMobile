#adb_utils.py

import subprocess


class AdbUtils:
    @staticmethod
    def get_app_version_from_adb(package: str, udid: str) -> str:
        result = subprocess.run(
            ["adb", "-s", udid, "shell", "dumpsys", "package", package],
            capture_output=True, text=True, check=True
        )
        for line in result.stdout.splitlines():
            if "versionName=" in line:
                return line.split("=")[1].strip()
        raise Exception(f"versionName не найден для пакета {package}")
