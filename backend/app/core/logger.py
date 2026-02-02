"""
Logging configuration for AITranslator.

This module provides centralized logging setup with support for multiple
log formats and configurable log levels.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from config import settings


def setup_logger(
    name: str = 'aitranslator',
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up and configure a logger instance.

    This function creates a configured logger with both console and file handlers,
    supporting both JSON and text log formats.

    Args:
        name: The name of the logger
        level: The logging level (defaults to settings.log_level)
        log_file: Path to the log file (defaults to settings.log_file)

    Returns:
        A configured logging.Logger instance

    Example:
        >>> logger = setup_logger('my_module')
        >>> logger.info('Application started')
    """
    # Use settings defaults if not provided
    if level is None:
        level = settings.log_level
    if log_file is None:
        log_file = settings.log_file

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatters
    if settings.log_format.lower() == 'json':
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO if settings.is_production else logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    This formatter outputs log records as JSON objects, making them
    easily parseable by log aggregation systems.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as JSON.

        Args:
            record: The log record to format

        Returns:
            JSON-formatted log string
        """
        import json

        log_data = {
            'timestamp': self.formatTime(record, '%Y-%m-%dT%H:%M:%S.%fZ'),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)
