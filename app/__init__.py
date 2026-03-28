"""
SmartBiz Flask Application Package
"""

import os
from flask import Flask
from flask_cors import CORS


def create_app():
    """Application factory for SmartBiz."""
    app = Flask(__name__, template_folder="templates")

    # Load configuration
    from app.config import get_config
    app.config.from_object(get_config())

    # Setup logging (before any request handling)
    from logging_config import setup_logging
    setup_logging(app)
    logger = app.logger

    logger.info(f"Starting SmartBiz in {app.config['ENV']} mode")

    # Enable CORS
    CORS(app)

    # Register security middleware
    from security import register_security_middleware
    register_security_middleware(app)

    # Register error handlers
    from error_handlers import register_error_handlers
    register_error_handlers(app)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Add health check endpoints
    @app.route("/health")
    def health():
        """Liveness probe - just check if app is running"""
        return {"status": "healthy"}, 200

    @app.route("/ready")
    def ready():
        """Readiness probe - check if database is accessible"""
        try:
            from app.database import get_client
            client = get_client()
            # Try a simple query to verify connection
            client.table("employees").select("id").limit(1).execute()
            return {"status": "ready"}, 200
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return {"status": "not_ready", "error": str(e)}, 503

    logger.info("SmartBiz application initialized successfully")
    return app

