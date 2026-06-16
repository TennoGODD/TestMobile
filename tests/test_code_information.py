# test_code_information.py

import allure
import time



@allure.feature("Информация по коду")
class TestCodeInformation:
    @allure.title("DMC Mobile. Получение информации по коду. Сканирование не агрегированного КМ")
    def test_barcode_scan_simulation(self, code_information_page):
        code_information_page.emulate_scan("0107665585002196215Ut,r7FhgAHj.93dGVz")
        time.sleep(5)


