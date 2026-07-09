# api_client.py
"""Создание заданий через REST API DMC.

Задание создаётся через официальный API (/api/v2/tasks/ — задание и
агрегация одной транзакцией через поле aggr_id), а НЕ прямой SQL-вставкой
в базу: служебные поля задания заполняет только внутренняя бизнес-логика
DMC, при вставке напрямую в БД они оставались NULL и ломали дальнейшую
работу с заданием.

Физические коды агрегатов (unit_id) здесь не создаём:
- КИГУ (уровень 0) DMC создаёт сама при контрольной печати — тесты берут
  его из БД (DatabaseClient.get_printed_aggregate);
- КИТУ (уровень 1) до сканирования в БД не существует — его код тесты
  генерируют сами (utils.generators.generate_kitu_code).
"""

from datetime import date

import requests

from utils.step_utils import shared_step


class DmcApiError(Exception):
    """Ошибка при обращении к REST API DMC."""


class DmcApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def _post(self, path: str, payload: dict):
        url = f"{self.base_url}{path}"
        try:
            # (5, 20) — 5 секунд на установку соединения, до 20 секунд на ответ
            resp = self.session.post(url, json=payload, timeout=(5, 20))
        except requests.RequestException as e:
            raise DmcApiError(f"Не удалось подключиться к API DMC ({url}): {e}")

        try:
            data = resp.json()
        except ValueError:
            raise DmcApiError(
                f"API DMC вернул не-JSON ответ ({url}), HTTP {resp.status_code}: {resp.text[:300]}"
            )

        if resp.status_code >= 400 or not data.get("success", True):
            raise DmcApiError(f"Ошибка API DMC ({url}), HTTP {resp.status_code}: {data.get('data', data)}")

        return data.get("data", data)

    def _create_task(self, gtin: str, line: int, amount: int, aggr_ids: list = None) -> int:
        today = date.today().isoformat()
        payload = {
            "product": gtin,
            "mandate": today,
            "line": line,
            "date": today,
            "amount": amount,
            # если чтение задания через GET /api/v2/tasks/{id} начнёт падать
            # с ошибкой валидации, вернуть поле: "marking_system": "CZ"
        }
        if aggr_ids:
            # пустой список aggr_id API считает ошибкой валидации (422),
            # поэтому поле добавляем только при наличии агрегации
            payload["aggr_id"] = aggr_ids

        task_data = self._post("/api/v2/tasks/", payload)
        taskid = task_data.get("taskid")
        if taskid is None:
            raise DmcApiError(f"API DMC не вернул taskid в ответе: {task_data}")
        return taskid

    def create_task_by_spec(self, gtin: str, line: int, amount: int, aggr_ids: list = None) -> int:

        levels = f", агрегация {aggr_ids}" if aggr_ids else ""
        with shared_step(f"Создание задания через API: gtin = {gtin}, количество КМ = {amount}{levels}"):
            return self._create_task(gtin, line, amount, aggr_ids=aggr_ids)

    def create_task(self, gtin: str, line: int, amount: int) -> int:
        with shared_step(f"Создание задания через API: gtin = {gtin}, количество КМ = {amount}"):
            return self._create_task(gtin, line, amount)

    def create_aggregation_task(self, gtin: str, line: int, amount: int, aggr_id: int) -> int:
        with shared_step(f"Создание задания с агрегацией через API: gtin = {gtin}, количество КМ = {amount}"):
            return self._create_task(gtin, line, amount, aggr_ids=[aggr_id])

    def create_two_level_aggregation_task(
            self,
            gtin: str,
            line: int,
            amount: int,
            aggr_level0_id: int,
            aggr_level1_id: int,
    ) -> int:
        with shared_step(f"Создание задания с двухуровневой агрегацией через API: gtin = {gtin}, количество КМ = {amount}"):
            return self._create_task(gtin, line, amount, aggr_ids=[aggr_level0_id, aggr_level1_id])

    # Физические коды агрегатов пока не создаём — DMC генерирует их сама,
    # ожидаемые коды тесты берут из БД. Если понадобится вернуть создание
    # своих кодов — раскомментировать и вызывать после _create_task:
    #
    # def _add_aggregate(self, taskid: int, unit_id: str, level: int):
    #     # именно /api/v2/aggregate/ в единственном числе — "aggregates" даёт 404
    #     self._post("/api/v2/aggregate/", {"taskid": taskid, "unit_id": unit_id, "level": level})
    #
    # @staticmethod
    # def _generate_unit_id(gtin: str) -> str:
    #     import random
    #     import string
    #     from datetime import datetime
    #     date_part = datetime.now().strftime("%d%m%y")
    #     random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    #     gtin_digits = gtin[-14:] if len(gtin) >= 14 else gtin.zfill(14)
    #     return f"010{gtin_digits}{date_part}{random_part}"
