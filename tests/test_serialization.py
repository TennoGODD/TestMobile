# test_serialization.py

from utils.step_utils import shared_step, shared_title
import allure
import pytest
import testit

from test_data.products import WATER, LINE, AGGR_LEVEL0_ID, AGGR_LEVEL1_ID



@allure.feature("Сериализация")
@allure.severity(allure.severity_level.BLOCKER)
@testit.labels("serialization")
class TestSerialization:
    @pytest.mark.task(amount=3)
    @shared_title("DMC Mobile. Сериализация. Сканирование КМ без агрегации")
    @testit.externalId("8")
    def test_serialization_without_aggregation(self, serialization_page, db, task):

        taskid = task

        codes = db.get_dm_codes(taskid)

        scanned = 0

        for code in codes:

            with shared_step(f"Сканируем код № {scanned + 1}"):
                with shared_step(f"Сканируем код {code}"):
                    serialization_page.emulate_scan(code)

                scanned += 1

                serialization_page.tap_task_warning_if_present()
                serialization_page.verify_serialization_data(
                    task_number=str(taskid),
                    gtin=WATER.gtin,
                    km_status=f"КМ {code} успешно отсканирован",
                    product_name=WATER.name,
                    total_km_label=f"Верифицировано из{len(codes)}",
                    verified_km_count=str(scanned)
                )

        serialization_page.tap_finish_button()
        serialization_page.assert_finish_dialog_displayed()
        serialization_page.cancel_finish_in_dialog()

        serialization_page.verify_serialization_data(
            task_number=str(taskid),
            gtin=WATER.gtin,
            km_status=f"КМ {codes[-1]} успешно отсканирован",
            product_name=WATER.name,
            total_km_label=f"Верифицировано из{len(codes)}",
            verified_km_count=str(len(codes))
        )

        serialization_page.tap_finish_button()
        serialization_page.assert_finish_dialog_displayed()
        serialization_page.confirm_finish_in_dialog()

        db.wait_for_task_status(taskid, target_status=9, timeout=30)

    @pytest.mark.task(amount=6, aggr_ids=[AGGR_LEVEL0_ID])
    @shared_title("DMC Mobile. Сериализация. Сканирование КМ с агрегацией (0 уровень) и контролем печати")
    @testit.externalId("9")
    def test_serialization_with_aggregation_level_0(self, serialization_page, db, task, printer_kigu):
        taskid = task

        codes = db.get_dm_codes(taskid)
        assert len(codes) == 6, "Должно быть 6 кодов"

        with shared_step(f"Сканируем код №1"):
            with shared_step(f"Сканируем код {codes[0]}"):
                serialization_page.emulate_scan(codes[0])

        serialization_page.assert_aggregation_dialog_displayed()

        aggregation_button = "МАСТ МИНЕРАЛЬНАЯ ВОДИЦА 6X"

        with shared_step(f"Нажать кнопку '{aggregation_button}'"):
            serialization_page.select_aggregation_packaging(aggregation_button)
            serialization_page.verify_serialization_data(scanned_in_aggr="1из6", completed_aggr="0 из 1")

        serialization_page.is_displayed(serialization_page.SHOW_PRINT_SETTINGS_BUTTON)
        serialization_page.is_displayed(serialization_page.COLLECT_BUTTON)

        for i, code in enumerate(codes[1:-1], start=2):
            with shared_step(f"Сканируем код №{i}"):
                with shared_step(f"Сканируем код {code}"):
                    serialization_page.emulate_scan(code)
                serialization_page.verify_serialization_data(
                    scanned_in_aggr=f"{i}из6",
                    completed_aggr="0 из 1",
                    check_action_buttons=True
                )

        last_code = codes[-1]
        with shared_step(f"Сканируем код №6: {last_code}"):
            with shared_step(f"Сканируем код {last_code}"):
                serialization_page.emulate_scan(last_code)

            serialization_page.assert_print_control_dialog_displayed(
                task_number=str(taskid),
                gtin=WATER.gtin
            )


        unit_id = printer_kigu.wait_for_code(timeout=30)

        for attempt in range(1, 3):
            with shared_step(f"Сканируем код агрегата (попытка {attempt})"):
                serialization_page.emulate_scan(unit_id)
            if db.wait_for_aggregate_status(taskid, target_status=30, level=0, timeout=5):
                break
        else:
            raise AssertionError(
                f"Агрегат 0 уровня по заданию {taskid} не перешёл в статус 30 после 2 попыток сканирования"
            )

        serialization_page.verify_serialization_data(
            task_number=str(taskid),
            gtin=WATER.gtin,
            km_status=f"КМ {codes[-1]} успешно отсканирован",
            product_name=WATER.name,
            total_km_label=f"Верифицировано из{len(codes)}",
            verified_km_count=str(len(codes)),
            scanned_in_aggr="0из6",
            completed_aggr="1 из 1",
            check_action_buttons=True
        )

        serialization_page.tap_finish_button()
        serialization_page.assert_finish_dialog_displayed()
        serialization_page.confirm_finish_in_dialog()
        db.wait_for_task_status(taskid, target_status=9, timeout=120)

    @pytest.mark.task(amount=12, aggr_ids=[AGGR_LEVEL0_ID, AGGR_LEVEL1_ID])
    @shared_title("DMC Mobile. Сериализация. Сканирование КМ с агрегацией (0 и 1 уровней) и контролем печати")
    @testit.externalId("19")
    def test_serialization_with_aggregation_levels_0_1(self, serialization_page, db, task, printer_kigu, printer_kitu):
        taskid = task

        codes = db.get_dm_codes(taskid)
        assert len(codes) == 12, "Должно быть 12 кодов"

        with shared_step(f"Сканируем код №1"):
            serialization_page.emulate_scan(codes[0])
            serialization_page.assert_aggregation_dialog_displayed()
            serialization_page.select_aggregation_packaging("МИНИ УПАКОВКА")
            serialization_page.verify_serialization_data(
                scanned_in_aggr="1из6", completed_aggr="0из2"
            )

        # 4. Сканировать КМ 2-5
        for i in range(1, 5): 
            code = codes[i]
            with shared_step(f"Сканируем код №{i + 1}: {code}"):
                serialization_page.emulate_scan(code)
                serialization_page.verify_serialization_data(
                    scanned_in_aggr=f"{i + 1}из6", completed_aggr="0из2"
                )

        # 5. Последний КМ первой партии (6-й)
        last_code_first = codes[5]
        with shared_step(f"Сканируем код №6: {last_code_first}"):
            serialization_page.emulate_scan(last_code_first)

        # 6. Окно контрольной печати для первого агрегата 0
        serialization_page.assert_print_control_dialog_displayed(
            task_number=str(taskid), gtin=WATER.gtin
        )

        # 7. Сканировать первый агрегат 0 — КИГУ перехватываем из задания печати
        unit_id_0_first = printer_kigu.wait_for_code(timeout=30)
        with shared_step(f"Сканируем агрегат 0 №1: {unit_id_0_first}"):
            serialization_page.emulate_scan(unit_id_0_first)
            serialization_page.verify_serialization_data(
                scanned_in_aggr="0из6", completed_aggr="1из2"
            )

        # 8. Сканировать КМ 7-11 (индексы 6..10), проверяя счётчики
        for i in range(6, 11):  # i = 6..10 → КМ №7..11
            code = codes[i]
            with shared_step(f"Сканируем КМ {i + 1}: {code}"):
                serialization_page.emulate_scan(code)
                serialization_page.verify_serialization_data(
                    scanned_in_aggr=f"{i - 5}из6", completed_aggr="1из2"
                )

        # 9. Последний КМ второй партии (12-й) – без проверки
        last_code_second = codes[11]
        with shared_step(f"Сканируем КМ 12: {last_code_second}"):
            serialization_page.emulate_scan(last_code_second)

            serialization_page.assert_print_control_dialog_displayed(
                task_number=str(taskid), gtin=WATER.gtin
            )

        # Второй агрегат 0 — снова перехватываем КИГУ из печати (второе задание
        # печати на порту уровня 0; первое было для КИГУ №1).
        unit_id_0_second = printer_kigu.wait_for_code(previous_count=1, timeout=30)
        with shared_step(f"Сканируем агрегат 0 №2: {unit_id_0_second}"):
            serialization_page.emulate_scan(unit_id_0_second)

            serialization_page.assert_print_control_dialog_displayed(
                task_number=str(taskid), gtin=WATER.gtin
            )

        # КИТУ уровня 1 — из отдельного эмулятора печати (порт уровня 1).
        with shared_step("Ожидание печати КИТУ уровня 1"):
            unit_id_1 = printer_kitu.wait_for_code(timeout=30)

        scanned_ok = False
        for attempt in range(1, 4):
            with shared_step(f"Сканируем агрегат 1 (попытка {attempt}): {unit_id_1}"):
                serialization_page.emulate_scan(unit_id_1)
                print(f"Отсканирован КИТУ: {unit_id_1}")

            if db.wait_for_aggregate(taskid, unit_id_1, timeout=5):
                scanned_ok = True
                break
            else:
                print(f"КИТУ {unit_id_1} не найден в БД после попытки {attempt}, повторяем сканирование...")

        if not scanned_ok:
            raise AssertionError(
                f"КИТУ {unit_id_1} не появился в БД после 3 попыток сканирования"
            )

        serialization_page.verify_serialization_data(
            task_number=str(taskid),
            gtin=WATER.gtin,
            product_name=WATER.name,
            total_km_label=f"Верифицировано из{len(codes)}",
            verified_km_count=str(len(codes)),
            scanned_in_aggr="0из6", 
            completed_aggr="0из2",
            check_action_buttons=True
        )

        serialization_page.tap_finish_button()
        serialization_page.assert_finish_dialog_displayed()
        serialization_page.confirm_finish_in_dialog()
        db.wait_for_task_status(taskid, target_status=9, timeout=120)