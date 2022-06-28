import datetime
from app.email import send_email
from .token import generate_confirmation_token, confirm_token
from flask import jsonify, make_response, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from flask import current_app

from app.models import User, db
from app.schema import UserFormSchema, UserSchema


user_form = UserFormSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# login_manager = LoginManager()

class UserData(object):

    def __init__(self, email, username, name, password, **kwargs):
        self.email = email
        self.username = username
        self.password = password
        self.name = name

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_password):
        return sha256.verify(password, hash_password)


class UserRegister(Resource):
    def post(self):
        """
                User signup
                ---
                description: User signup
                parameters:
                    - name: User
                      in: body
                      type: string
                      required: true
                      schema:
                        $ref: '#/definitions/User_sign_up'
                responses:
                  201:
                    description: User {} was created
                  400:
                    description: Bad request
              """
        try:
            args = request.json
            error = user_form.validate(args)

            if error:
                return make_response(jsonify({"message": f"{error}"}), 400)

            user = UserData(**args)
            user.password = UserData.generate_hash(args['password'])
            if User.query.filter_by(email=user.email).first():
                return make_response(jsonify({"message": "email already exists"}), 403)
            elif User.query.filter_by(username=user.username).first():
                return make_response(jsonify({"message": "username already used"}), 403)
            me = User(username=user.username, password=user.password, email=user.email, name=user.name, confirmed=False)
            db.session.add(me)
            db.session.commit()
            token = generate_confirmation_token(me.email)
            confirm_url = url_for('Confirm', token=token, _external=True)
            html = render_template('user/activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            return make_response(jsonify({'message': 'User {0} was created'.format(user.username)}),201)
        except Exception as e:
            current_app.logger.error(f"{e}")
            db.session.rollback()
            return make_response(jsonify({"error": f"Server Error {e}"}), 500)

    @staticmethod
    def get():
        try:
            result = User.query.all()
            return users_schema.dump(result)
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return make_response(jsonify({"error": "Server Error"}), 500)

class UserLogin(Resource):
    def __init__(self):
        self.request_parse = reqparse.RequestParser()
        self.request_parse.add_argument(
            'username', type=str, required=True, help='please input username', location=['json', 'form']
        )
        self.request_parse.add_argument(
            'password', type=str, required=True, help='please input password', location=['json', 'form']
        )

    def post(self):
        """
               Login
               ---
               description: User login
               parameters:
                   - name: Login
                     in: body
                     type: string
                     schema:
                       $ref: '#/definitions/User_login'
               responses:
                   202:
                       description: successfully logged in
                   401:
                       description: wrong credentintials provided
                   404:
                       description: User doesn't exist
               """
        args = self.request_parse.parse_args()
        username = args['username']
        password = args['password']
        if not username.replace(" ", ""):
            return {"message": "input valid username"}, 400
        elif not password.replace(" ", ""):
            return {"message": "input password it is empty"}, 400
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            return {"message": 'User {} doesn\'t exist'.format(args['username'])}, 404

        if UserData.verify_hash(args['password'], user.password):
            # access_token = create_access_token(identity=user.username)
            # refresh_token = create_refresh_token(identity=user.username)
            return make_response(jsonify( {
                       'message': 'Logged in as {}'.format(user.username),
                    #    'access_token': access_token,
                    #    'refresh_token': refresh_token
                   }), 202)
        else:
            return {'message': 'wrong credentials provided'}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 202

class ConfirmEmail(Resource):
    def get(self, token):
        try:
            email = confirm_token(token)
            user = User.query.filter_by(email=email).first_or_404()
            if user.confirmed:
                return make_response(jsonify({"message":f"Account already confirmed. Please login."}), 200)
            else:
                user.confirmed = True
                user.confirmed_on = datetime.datetime.now()
                db.session.add(user)
                db.session.commit()
                return make_response(jsonify({"message":'You have confirmed your account. Thanks!'}), 200)
        except Exception as e:
            current_app.logger.error(f"{e}")
            db.session.rollback()
            return make_response(jsonify({"error":f"The confirmation link is invalid or has expired."}), 401)


class Unconfirmed(Resource):
    @login_required
    def get():
        if current_user.is_active:
            return make_response(jsonify({"message":'You have confirmed your account. Thanks!'}), 200)
        return render_template('user/unconfirmed.html')