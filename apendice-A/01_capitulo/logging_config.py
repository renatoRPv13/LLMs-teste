# src/utils/logging_config.py
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


def setup_logging(
        log_level: str = "INFO",
        log_dir: Optional[Path] = None,
        log_to_file: bool = True,
        log_to_console: bool = True,
) -> None:
    """Configura o logging para a aplicação."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(log_format)
        root_logger.addHandler(console_handler)

    if log_to_file:
        if log_dir is None:
            log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"clinical_rag_{today}.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10_000_000,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(log_format)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado."""
    logger = logging.getLogger(name)
    logger.propagate = True
    return logger
