"""
Error handlers for SmartBiz application.
"""

from flask import jsonify


def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Not Found", "message": "The requested resource does not exist"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(f"Internal Server Error: {error}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors."""
        return jsonify({"error": "Forbidden", "message": "You do not have permission to access this resource"}), 403
    
    return app
