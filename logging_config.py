"""
Centralized logging configuration for production-ready deployment.
Supports both console and file logging with JSON format in production.
"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime


def setup_logging(app):
    """Configure logging for the Flask application"""
    flask_env = os.getenv("FLASK_ENV", "production").lower()
    log_level = logging.DEBUG if flask_env == "development" else logging.INFO

    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)

    # Remove default Flask logger
    app.logger.handlers = []

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler (always)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Format: Include timestamp, level, logger name, and message
    if flask_env == "production":
        # JSON format for production
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (rotation) - only in production
    if flask_env == "production":
        log_file = os.path.join("logs", "smartbiz.log")
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=10,  # Keep 10 backup files
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            app.logger.warning(f"Failed to setup file logging: {e}")

    # Set Flask app logger to use root logger
    app.logger = logging.getLogger("smartbiz")
    app.logger.setLevel(log_level)

    return root_logger


def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)
