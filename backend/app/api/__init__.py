"""
API routes for AITranslator.

This module contains all API endpoints and route handlers.
"""

from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes to register them with the blueprint
from app.api import translate_routes, health_routes

__all__ = ['api_bp']
