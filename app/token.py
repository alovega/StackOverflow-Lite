from flask import current_app
import jwt
from datetime import datetime, timezone, timedelta
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

def generate_confirmation_token(email):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    except Exception as e:
        current_app.logger.error(f"{e}")
        return Exception


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
        return Exception


def generate_auth_token(email, expiration=3600*15):
    try:
        return str(jwt.encode({"email": email, "exp": datetime.now(tz=timezone.utc)+ timedelta(days=15)}, f"'{current_app.config['SECRET_KEY']}'", algorithm="HS256"))
    except Exception as s:
        current_app.logger.error(f"{s}")
        return Exception


def verify_token(token):
    try:
        email = jwt.decode(token, f"'{current_app.config['SECRET_KEY']}'", algorithms=['HS256']).get('email')
        return email
    except jwt.ExpiredSignatureError as e:
        current_app.logger.error(f"{e}")
        return Exception
    except jwt.DecodeError as e:
        current_app.logger.error(f"{e}")
        return Exception

    