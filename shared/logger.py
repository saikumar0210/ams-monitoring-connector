"""
shared/logger.py

Centralized logger factory for the AMS Monitoring Connector.

Provides a consistently formatted logger with stdout output.
Format: <timestamp> | <level> | <logger_name> | <message>

Usage:
    from shared.logger import get_logger
    logger = get_logger("module.name")
"""
import logging
import sys


def get_logger(
    name: str
) -> logging.Logger:

    # Reuse an existing logger if it has already been configured for this name
    # This prevents duplicate handlers when the same module is imported multiple times
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    # Set minimum log level to INFO — DEBUG messages will be suppressed
    logger.setLevel(logging.INFO)

    # Define a consistent log format across all modules
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Write all logs to stdout so they appear in Render / container logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevent log messages from bubbling up to the root logger (avoids duplicate output)
    logger.propagate = False

    return logger
