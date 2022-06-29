from functools import wraps

from flask import current_app, jsonify, make_response, request

from flask_jwt_extended import current_user, get_jwt_identity

from app.models import User

from .token import verify_token


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return make_response(jsonify({"Error": "Please Confirm your account first"}), 401)
        return func(*args, **kwargs)

    return decorated_function

def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return make_response(jsonify({
                "message": "Authentication Token missing!",
                "data": None,
                "error": "Unauthorized"
            }), 401)

        try:
            email = verify_token(token)
            current_user = User.query.filter_by(email=email).first()
            if current_user is None:
                return make_response(jsonify({
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
                }), 401)
            if not current_user.confirmed:
                return make_response(jsonify({
                "message": "User not Verified!",
                "data": None,
                "error": "Unauthorized"
                }), 401)

        except Exception as e:
            current_app.logger.error(f"{e}")
            return make_response(jsonify({
                "message": "Something went wrong",
                "data": None,
            }), 500)

        return func(current_user, *args, **kwargs)

    return decorated_function