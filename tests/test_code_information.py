# test_code_information.py

from utils.step_utils import shared_step, shared_title
import allure
import testit

from test_data.products import WATER



@allure.feature("Информация по коду")
@allure.severity(allure.severity_level.CRITICAL)
@testit.labels("code-information")
class TestCodeInformation:
    @shared_title("DMC Mobile. Получение информации по коду. Сканирование не агрегированного КМ")
    @testit.externalId("487")
    def test_scan_non_aggregated_km(self, code_information_page):
        with shared_step("Сканирование не агрегированного КМ"):
            code_information_page.emulate_scan('0107665585002196215:Br"pRINgH+W')
        code_information_page.swipe_up(0.1)
        code_information_page.verify_scanned_data(
            code='0107665585002196215:Br"pRINgH+W',
            aggr_info="Не в агрегате",
            gtin=f"{WATER.gtin} ",
            product_name=WATER.name,
            status="Верифицирован (Сериализован)",
            production_date="29.06.2026",
            serialization_date= "29.06.2026",
            emission_date="19.06.2026",
            task_number="1351944",
            task_date="29.06.2026",
            task_status="Идёт процесс сериализации на линии",
        )

    @shared_title("DMC Mobile. Получение информации по коду. Сканирование агрегированного КМ")
    @testit.externalId("488")
    def test_scan_aggregated_km(self, code_information_page):
        with shared_step("Сканирование агрегированного КМ"):
            code_information_page.emulate_scan("0107665585002196215)KnUifb!k!.R")

        code_information_page.swipe_up(0.1)
        code_information_page.verify_scanned_data(
            code="0107665585002196215)KnUifb!k!.R",
            aggr_info="0007665585002196067220626YfCsqxA3",
            gtin=f"{WATER.gtin} ",
            product_name=WATER.name,
            status="Верифицирован (Сериализован)",
            production_date="18.06.2026",
            serialization_date= "22.06.2026",
            emission_date="18.06.2026",
            task_number="1351646",
            task_date="18.06.2026",
            task_status="Требуется отправить отчёт о нанесении КМ",
        )


