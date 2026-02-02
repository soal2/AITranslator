"""
Health check and status API routes.

This module contains health check endpoints for monitoring
and service status.
"""

from flask import Blueprint, jsonify
from config import settings

from app.api import api_bp
from app.core import setup_logger

logger = setup_logger(__name__)

# Create health check blueprint
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    This endpoint returns the health status of the service,
    useful for load balancers and monitoring systems.

    Response (200):
        {
            "status": "healthy",
            "service": "aitranslator",
            "environment": "development"
        }
    """
    response = {
        'status': 'healthy',
        'service': 'aitranslator',
        'environment': settings.app_env,
        'version': '1.0.0'
    }
    return jsonify(response), 200


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """
    Readiness check endpoint.

    This endpoint checks if the service is ready to accept requests.
    It can be extended to check database connections, external services, etc.

    Response (200):
        {
            "status": "ready",
            "checks": {
                "llm_service": "available"
            }
        }

    Response (503):
        {
            "status": "not_ready",
            "checks": {
                "llm_service": "unavailable"
            }
        }
    """
    checks = {
        'llm_service': 'available'
    }

    all_ready = all(status == 'available' for status in checks.values())

    status_code = 200 if all_ready else 503
    response = {
        'status': 'ready' if all_ready else 'not_ready',
        'checks': checks
    }

    return jsonify(response), status_code


@health_bp.route('/info', methods=['GET'])
def service_info():
    """
    Service information endpoint.

    This endpoint returns information about the service,
    including configuration and capabilities.

    Response (200):
        {
            "name": "AITranslator",
            "version": "1.0.0",
            "description": "AI-powered Chinese to English translation service",
            "endpoints": [
                {"path": "/api/translate", "method": "POST", "description": "Translate text"},
                {"path": "/api/health", "method": "GET", "description": "Health check"}
            ]
        }
    """
    response = {
        'name': settings.app_name,
        'version': '1.0.0',
        'description': 'AI-powered Chinese to English translation service',
        'environment': settings.app_env,
        'endpoints': [
            {
                'path': '/api/translate',
                'method': 'POST',
                'description': 'Translate Chinese text to English'
            },
            {
                'path': '/api/health',
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            {
                'path': '/api/ready',
                'method': 'GET',
                'description': 'Readiness check endpoint'
            },
            {
                'path': '/api/info',
                'method': 'GET',
                'description': 'Service information'
            }
        ]
    }

    return jsonify(response), 200


# Register blueprint with API blueprint
api_bp.register_blueprint(health_bp)
