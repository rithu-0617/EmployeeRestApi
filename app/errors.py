"""
Global error handlers.
"""
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Register application-wide error handlers."""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized", "message": str(error)}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden", "message": str(error)}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found", "message": str(error)}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"error": "Unprocessable entity", "message": str(error)}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.name, "message": error.description}), error.code
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500
