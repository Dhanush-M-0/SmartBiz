"""
Security middleware and headers for SmartBiz application.
"""


def register_security_middleware(app):
    """Register security middleware and headers."""
    
    @app.after_request
    def set_security_headers(response):
        """Add security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' https:"
        return response
    
    return app
