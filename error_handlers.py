"""
Global error handlers for the Flask application.
Provides consistent error responses and logging.
"""

from flask import jsonify
from logging_config import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):
    """Register global error handlers with the Flask app"""

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        logger.warning(f"Bad request: {error}")
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": str(error.description) if hasattr(error, "description") else str(error),
                }
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return (
            jsonify(
                {
                    "error": "Not Found",
                    "message": "The requested resource does not exist",
                }
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        logger.error(f"Internal server error: {error}", exc_info=True)
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            ),
            500,
        )

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            ),
            500,
        )
