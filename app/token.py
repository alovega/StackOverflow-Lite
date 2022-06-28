from flask import current_app, jsonify, make_response

from itsdangerous import BadSignature, Serializer, SignatureExpired, URLSafeTimedSerializer

def generate_confirmation_token(email):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    
    except Exception as e:
        current_app.logger.error(f"{e}")
        return {"Error": "Error while generating token"}


def confirm_token(token, expiration=1):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age= expiration
        )
        return email
    except SignatureExpired as e:
        current_app.logger.error(f"{e}")
        return {"Error": "token expired"}
    except BadSignature as e:
        current_app.logger.error(f"{e}")
        return {"Error": "Invalid token provided"}


def generate_auth_token(email, expiration= 3600 * 15):
    serializer = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
    return serializer.dumps(email= email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def verify_token(token):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
        return email
    except SignatureExpired as e:
        current_app.logger.error(f"{e}")
        return {"Error": "token expired"}
    except BadSignature as e:
        current_app.logger.error(f"{e}")
        return {"Error": "Invalid token provided"}

    