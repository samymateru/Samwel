import logging
import sys
from threading import Lock
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerSingleton:
    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, name="app_logger", level=logging.INFO):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="app_logger", level=logging.INFO):
        if self._initialized:
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # Prevent duplicate handlers in reloads
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 🧩 Production-grade formatter (adds file, line, func)
        self.formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self._initialized = True

    def add_console_handler(self, level=logging.INFO):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
        return self

    def add_file_handler(self, filepath: str = "logs/app.log", level=logging.INFO):
        # Ensure log directory exists
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filepath,
            maxBytes=10_000_000,  # 10 MB
            backupCount=5,        # Keep 5 rotated logs
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        return self

    def set_level(self, level):
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
        return self

    def set_formatter(self, formatter: logging.Formatter):
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)
        return self

    def get_logger(self) -> logging.Logger:
        return self.logger


# ✅ Initialize global production logger
global_logger = (
    LoggerSingleton(level=logging.INFO)
    .add_console_handler()
    .add_file_handler("logs/app.log")
    .get_logger()
)
