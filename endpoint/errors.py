from flask import jsonify
from flask_limiter.errors import RateLimitExceeded


def register_error_handlers(app):
    @app.errorhandler(RateLimitExceeded)
    def ratelimit_handler(e):
        return jsonify(
            {
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please wait a minute before trying again.",
            }
        ), 429

    # @app.errorhandler(404)
    # def not_found(e):
    #     return jsonify(
    #         {"error": "Not Found", "message": "The requested resource was not found."}
    #     ), 404
