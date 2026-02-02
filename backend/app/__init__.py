"""
AITranslator Flask application factory.

This module creates and configures the Flask application instance,
registering all blueprints, middleware, and error handlers.
"""

from typing import NoReturn

from flask import Flask
from flask_cors import CORS

from app.api import api_bp
from app.core import (
    AITranslatorError,
    setup_logger,
    create_error_response
)
from config import settings

logger = setup_logger(__name__)


def create_app(config_override: dict | None = None) -> Flask:
    """
    Create and configure the Flask application.

    This function implements the application factory pattern, allowing
    for easy testing and multiple application instances if needed.

    Args:
        config_override: Optional dictionary of configuration overrides

    Returns:
        Configured Flask application instance

    Example:
        >>> app = create_app()
        >>> app.run(host='0.0.0.0', port=5000)
    """
    # Create Flask app
    app = Flask(
        __name__,
        static_folder=None,
        template_folder=None
    )

    # Configure application
    _configure_app(app, config_override)

    # Initialize extensions
    _init_extensions(app)

    # Register blueprints
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    # Log application startup
    logger.info(
        f"Application '{settings.app_name}' initialized in "
        f"'{settings.app_env}' mode"
    )

    return app


def _configure_app(app: Flask, config_override: dict | None) -> None:
    """
    Configure the Flask application.

    Args:
        app: Flask application instance
        config_override: Optional configuration overrides
    """
    # Load configuration from settings
    app.config['DEBUG'] = settings.app_debug
    app.config['TESTING'] = settings.app_env == 'testing'
    app.config['JSON_AS_ASCII'] = False  # Support Unicode in JSON

    # Apply any configuration overrides
    if config_override:
        app.config.update(config_override)


def _init_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions.

    Args:
        app: Flask application instance
    """
    # Enable CORS for all routes
    CORS(app, resources={
        r'/api/*': {
            'origins': '*',
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization']
        }
    })


def _register_blueprints(app: Flask) -> None:
    """
    Register application blueprints.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(api_bp)
    logger.debug("Registered API blueprint")


def _register_error_handlers(app: Flask) -> None:
    """
    Register global error handlers.

    Args:
        app: Flask application instance
    """

    @app.errorhandler(AITranslatorError)
    def handle_app_error(error: AITranslatorError) -> tuple[dict, int]:
        """
        Handle custom AITranslator errors.

        Args:
            error: The AITranslatorError instance

        Returns:
            Tuple of (response dict, status code)
        """
        logger.warning(
            f"App error: {error.error_code} - {error.message}"
        )

        response_data = {
            'error': error.error_code,
            'message': error.message
        }

        # Include details only in non-production environments
        if error.details and not settings.is_production:
            response_data['details'] = error.details

        return response_data, error.status_code

    @app.errorhandler(400)
    def handle_bad_request(error: Exception) -> tuple[dict, int]:
        """Handle 400 Bad Request errors."""
        logger.warning(f"Bad request: {error}")
        return create_error_response(
            error='BAD_REQUEST',
            message='The request could not be understood',
            status_code=400
        )

    @app.errorhandler(404)
    def handle_not_found(error: Exception) -> tuple[dict, int]:
        """Handle 404 Not Found errors."""
        logger.warning(f"Not found: {error}")
        return create_error_response(
            error='NOT_FOUND',
            message='The requested resource was not found',
            status_code=404
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error: Exception) -> tuple[dict, int]:
        """Handle 405 Method Not Allowed errors."""
        logger.warning(f"Method not allowed: {error}")
        return create_error_response(
            error='METHOD_NOT_ALLOWED',
            message='The method is not allowed for the requested URL',
            status_code=405
        )

    @app.errorhandler(500)
    def handle_internal_error(error: Exception) -> tuple[dict, int]:
        """Handle 500 Internal Server Error."""
        logger.exception(f"Internal server error: {error}")
        return create_error_response(
            error='INTERNAL_ERROR',
            message='An internal server error occurred',
            status_code=500
        )

    logger.debug("Registered error handlers")


# Global debug setting for error handlers
settings_debug = settings.app_debug


def main() -> NoReturn:
    """
    Entry point for running the application directly.

    This function is intended for development use only.
    For production deployment, use a WSGI server like gunicorn or uwsgi.
    """
    app = create_app()

    logger.info(f"Starting server on {settings.app_host}:{settings.app_port}")

    app.run(
        host=settings.app_host,
        port=settings.app_port,
        debug=settings.app_debug
    )


if __name__ == '__main__':
    main()
