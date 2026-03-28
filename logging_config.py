"""
Logging configuration for SmartBiz application.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(app):
    """Configure logging for the Flask app."""
    # Remove default Flask logger handlers
    if app.logger.hasHandlers():
        for handler in app.logger.handlers[:]:
            app.logger.removeHandler(handler)
    
    # Create console handler with JSON formatter
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    
    # Set log level based on environment
    log_level = logging.DEBUG if app.debug else logging.INFO
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)
    
    return app.logger
