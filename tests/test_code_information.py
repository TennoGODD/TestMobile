# test_code_information.py

import allure
import testit
import time



@allure.feature("Информация по коду")
class TestCodeInformation:
    @allure.title("DMC Mobile. Получение информации по коду. Сканирование не агрегированного КМ")
    @testit.workItemIds("487")
    @testit.externalId("")
    @allure.title("DMC Mobile. Получение информации по коду. Сканирование не агрегированного КМ")
    def test_scan_non_aggregated_km(self, code_information_page):
        code_information_page.emulate_scan("0107665585002196215Ut,r7FhgAHj.93dGVz")
        code_information_page.swipe_up(0.1)
        code_information_page.verify_scanned_data(
            code="0107665585002196215Ut,r7FhgAHj.",
            aggr_info="Не в агрегате",
            gtin="07665585002196 ",
            product_name="МАСТ Минеральная водица",
            status="Распечатан",
            production_date="04.06.2026",
            emission_date="28.05.2026",
            task_number="1351422",
            task_date="04.06.2026",
            task_status="Требуется отправить отчёт о нанесении КМ",
        )

    @allure.title("DMC Mobile. Получение информации по коду. Сканирование агрегированного КМ")
    @testit.workItemIds("488")
    @testit.externalId("")
    @allure.title("DMC Mobile. Получение информации по коду. Сканирование не агрегированного КМ")
    def test_scan_aggregated_km(self, code_information_page):
        code_information_page.emulate_scan("0107665585002196215)KnUifb!k!.R93dGVz")
        code_information_page.swipe_up(0.1)
        code_information_page.verify_scanned_data(
            code="0107665585002196215)KnUifb!k!.R",
            aggr_info="0007665585002196067220626YfCsqxA3",
            gtin="07665585002196 ",
            product_name="МАСТ Минеральная водица",
            status="Верифицирован (Сериализован)",
            production_date="18.06.2026",
            serialization_date= "22.06.2026",
            emission_date="18.06.2026",
            task_number="1351646",
            task_date="18.06.2026",
            task_status="Требуется отправить отчёт о нанесении КМ",
        )


