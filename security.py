"""
Security middleware for Flask application.
Adds security headers and enforces security settings.
"""

from flask import request
from logging_config import get_logger

logger = get_logger(__name__)


def register_security_middleware(app):
    """Register security middleware with the Flask app"""

    @app.before_request
    def before_request():
        """Pre-request security checks"""
        # Check request size limit (10MB)
        max_content_length = 10 * 1024 * 1024
        if request.content_length and request.content_length > max_content_length:
            logger.warning(f"Request too large: {request.content_length} bytes from {request.remote_addr}")
            return "Request too large", 413

    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Clickjacking protection
        response.headers["X-Frame-Options"] = "DENY"

        # XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Feature policy
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Content Security Policy (basic)
        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"

        # HSTS (only in production)
        if app.config.get("SECURE_SSL_REDIRECT"):
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response
