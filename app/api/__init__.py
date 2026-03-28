"""
API Blueprint Registration
Registers all RESTful API endpoints under /api prefix
"""

from flask import Blueprint
from . import employees, tasks

def register_api_blueprints(app):
    """Register all API blueprints with the app"""
    app.register_blueprint(employees.bp)
    app.register_blueprint(tasks.bp)
