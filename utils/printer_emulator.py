# printer_emulator.py
"""Эмулятор сетевого принтера (TSPL) для перехвата кодов агрегатов.

При контроле печати агрегата приложение отправляет на принтер задание TSPL,
в котором зашит код агрегата (unit_id), сгенерированный самим DMC. Для
агрегатов, которых нет в БД заранее (КИТУ, уровень 1), это единственный
способ узнать реальный код для сканирования.

Эмулятор поднимает TCP-сервер, принимает задания печати в фоновом потоке и
складывает извлечённые коды. Настраивается host/port, чтобы приложение
печатало на машину с тестами (Порт сервиса печати в настройках ТСД).
"""

import re
import socket
import threading
import time


class PrinterEmulator:
    # код агрегата идёт в TSPL после префикса ~1, например
    # "~10107665585002196068080726XQU3fBqM" → 0107665585002196068080726XQU3fBqM
    _CODE_RE = re.compile(r'~1([^"\r\n]+)')

    def __init__(self, host: str = "0.0.0.0", port: int = 9103):
        self.host = host
        self.port = port
        self._server = None
        self._thread = None
        self._running = False
        self._codes = []
        self._raw_payloads = []  # сырые задания печати — для отладки формата
        self._lock = threading.Lock()

    def start(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen()
        self._server.settimeout(0.5)
        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._server:
            try:
                self._server.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=2)

    def received_count(self) -> int:
        with self._lock:
            return len(self._codes)

    def wait_for_code(self, previous_count: int = 0, timeout: int = 30, poll_interval: float = 0.3) -> str:
        """Ждёт новое задание печати и возвращает код агрегата из него.

        previous_count — сколько кодов было получено ДО ожидаемой печати
        (обычно printer.received_count(), снятый перед действием, которое
        вызывает печать нужного агрегата). Возвращается последний код.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if len(self._codes) > previous_count:
                    return self._codes[-1]
            time.sleep(poll_interval)
        raise TimeoutError(
            f"Принтер-эмулятор не получил новый код за {timeout} сек "
            f"(было {previous_count}, стало {self.received_count()})"
        )

    def _serve(self):
        while self._running:
            try:
                conn, _ = self._server.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with conn:
                conn.settimeout(2)
                chunks = []
                try:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        chunks.append(data)
                except socket.timeout:
                    pass
            payload = b"".join(chunks).decode("utf-8", errors="ignore")
            code = self._extract_code(payload)
            with self._lock:
                self._raw_payloads.append(payload)
                if code:
                    self._codes.append(code)

    def last_payload(self):
        """Последнее сырое задание печати — удобно приложить в отчёт для отладки формата."""
        with self._lock:
            return self._raw_payloads[-1] if self._raw_payloads else None

    @classmethod
    def _extract_code(cls, payload: str):
        match = cls._CODE_RE.search(payload)
        if not match:
            return None
        code = match.group(1)
        # внутренние ~1 (FNC1/GS1-разделитель в TSPL) → байт GS (\x1d), как на
        # реальной этикетке: у КИГУ это разделитель между unit_id и криптохвостом,
        # у КИТУ таких вставок нет — код остаётся как есть.
        return code.replace("~1", "\x1d")
