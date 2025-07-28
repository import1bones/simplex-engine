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
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    level=logging.INFO
)

def log(message: str, level: str = "INFO"):
    """
    Log a message with a given level.
    Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    logger = logging.getLogger("simplex-engine")
    logger.log(_LOG_LEVELS.get(level.upper(), logging.INFO), message)
