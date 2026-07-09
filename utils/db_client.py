# db_client.py
"""Read-only доступ к базе DMC: статусы заданий, коды маркировки.

Создание заданий здесь намеренно отсутствует — оно идёт через REST API
(см. utils/api_client.py), потому что прямые SQL-вставки оставляли NULL
в служебных полях, которые заполняет только бизнес-логика DMC.
"""

import time

import psycopg2

from utils.step_utils import shared_step


class DatabaseClient:
    def __init__(self, host, port, dbname, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )

    def close(self):
        if self.conn:
            self.conn.close()

    def _fetchone(self, query, params) -> tuple:
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                row = cur.fetchone()
            self.conn.commit()
            return row
        except Exception:
            self.conn.rollback()
            raise

    def _fetchall(self, query, params) -> list:
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
            self.conn.commit()
            return rows
        except Exception:
            self.conn.rollback()
            raise

    def wait_for_task_status(self, taskid: int, target_status: int = 6, timeout: int = 60, poll_interval: float = 2.0) -> int:
        with shared_step(f"Ждём, пока статус задания {taskid} станет {target_status}"):
            start_time = time.monotonic()
            query = "SELECT status FROM tasks WHERE taskid = %s;"
            while True:
                row = self._fetchone(query, (taskid,))
                if row is None:
                    raise ValueError(f"Задание с taskid={taskid} не найдено")
                current_status = row[0]
                if current_status == target_status:
                    return current_status
                if time.monotonic() - start_time > timeout:
                    raise TimeoutError(
                        f"Задание {taskid} не перешло в статус {target_status} за {timeout} секунд. Текущий статус: {current_status}"
                    )
                time.sleep(poll_interval)

    def get_dm_codes(self, taskid: int) -> list:
        query = "SELECT dm FROM dm WHERE taskid = %s;"
        return [row[0] for row in self._fetchall(query, (taskid,))]

    def wait_for_aggregate(self, taskid: int, unit_id: str, timeout: int = 5, poll_interval: float = 0.5) -> bool:
        """Проверяет, появился ли агрегат unit_id в БД задания.

        Возвращает True/False (не бросает исключение) — чтобы вызывающий код
        мог повторить сканирование, если код ещё не записался.
        """
        start_time = time.monotonic()
        query = "SELECT 1 FROM aggregates WHERE taskid = %s AND unit_id = %s;"
        while True:
            if self._fetchone(query, (taskid, unit_id)) is not None:
                return True
            if time.monotonic() - start_time > timeout:
                return False
            time.sleep(poll_interval)

    def wait_for_aggregate_status(self, taskid: int, target_status: int, level: int = 0,
                                  timeout: int = 5, poll_interval: float = 0.5) -> bool:
        """Ждёт, пока у задания появится агрегат заданного уровня в нужном статусе.

        Возвращает True/False (не бросает) — чтобы вызывающий код мог повторить
        сканирование, если статус ещё не сменился.
        """
        start_time = time.monotonic()
        query = "SELECT 1 FROM aggregates WHERE taskid = %s AND level = %s AND status = %s LIMIT 1;"
        while True:
            if self._fetchone(query, (taskid, level, target_status)) is not None:
                return True
            if time.monotonic() - start_time > timeout:
                return False
            time.sleep(poll_interval)

    def wait_for_aggregate_count(self, taskid: int, target_status: int, level: int, expected_count: int,
                                 timeout: int = 5, poll_interval: float = 0.5) -> bool:
        """Ждёт, пока число агрегатов заданного уровня в нужном статусе достигнет expected_count.

        Нужно, когда агрегатов одного уровня несколько (например, два КИГУ):
        проверка «есть хотя бы один в статусе 30» сработала бы уже после первого,
        поэтому сверяем именно количество. Возвращает True/False (не бросает).
        """
        start_time = time.monotonic()
        query = "SELECT COUNT(*) FROM aggregates WHERE taskid = %s AND level = %s AND status = %s;"
        while True:
            if self._fetchone(query, (taskid, level, target_status))[0] >= expected_count:
                return True
            if time.monotonic() - start_time > timeout:
                return False
            time.sleep(poll_interval)

    def get_printed_aggregate(self, taskid: int, level: int = 0, exclude_unit_id: str = None,
                              timeout: int = 10, poll_interval: float = 0.5) -> tuple:
        """Возвращает (unit_id, криптохвост dm_93) агрегата в статусе «Распечатан» (20).

        После контрольной печати именно этот агрегат ожидает сканирования.
        exclude_unit_id позволяет пропустить уже отсканированный ранее агрегат.
        """
        with shared_step(f"Получаем из БД распечатанный агрегат уровня {level} задания {taskid}"):
            start_time = time.monotonic()
            query = "SELECT unit_id, dm_93 FROM aggregates WHERE taskid = %s AND level = %s AND status = 20;"
            while True:
                rows = [row for row in self._fetchall(query, (taskid, level))
                        if row[0] and row[0] != exclude_unit_id]
                if rows:
                    unit_id, crypto_tail = rows[0]
                    return unit_id, crypto_tail
                if time.monotonic() - start_time > timeout:
                    raise TimeoutError(
                        f"У задания {taskid} нет агрегата уровня {level} "
                        f"в статусе 20 (распечатан) за {timeout} секунд"
                    )
                time.sleep(poll_interval)
