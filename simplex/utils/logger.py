"""
Simple logger utility for developer visibility.
Uses Python's built-in logging module for reliability and extensibility.
"""

import logging

_LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s] %(message)s",
    level=logging.INFO,
)


def log(message: str, level: str = "INFO"):
    """
    Log a message with a given level.
    Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    Automatically includes module and function name in the log output.
    """
    logger = logging.getLogger("simplex-engine")
    # stacklevel=2 ensures the caller's module/function is shown (Python 3.8+)
    logger.log(_LOG_LEVELS.get(level.upper(), logging.INFO), message, stacklevel=2)
