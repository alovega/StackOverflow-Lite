from flask_restful import Resource, fields, reqparse,marshal_with
from passlib.hash import pbkdf2_sha256 as sha256
from models.models import AppDb
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity)

AppDao = AppDb('development')

class UserData(object):

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserRegister(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='please input email', location='json')
        self.reqparse.add_argument('username', type=str, required=True, help='please input username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='please input password', location='json')
        super(UserRegister, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']

        if not email.replace(" ", ""):
            return {"message":"email not valid"}, 400
        elif not password.replace(" ", ""):
            return {"message":"input password it is empty"}, 400
        elif not username.replace(" ", ""):
            return {"message":"input valid username"}, 400

        user = UserData(email=email, username=username, password=password)


        if AppDao.check_user_exist_by_email(user.email):
            return {"message": "Email already used"}, 409
        elif AppDao.check_user_exist_by_username(user.username):
            return {"message": "username already used pick another one"}, 409

        user.password = UserData.generate_hash(password)
        AppDao.insert_user(user)
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return {
            'message': 'User {0} was created'.format(username),
            'access_token': access_token,
            'refresh_token':refresh_token
        }


    def get(self):
        result = AppDao.get_all()
        return result


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='please input username', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='please input password', location='json')

    def post(self):
        args = self.reqparse.parse_args()
        user = AppDao.get_user_by_username(args['username'])

        if not user:
            return {"message": 'User {} doesn\'t exist'.format(args['username'])}


        if UserData.verify_hash(args['password'], user[0]['password']):
            access_token = create_access_token (identity=user[0]['username'])
            refresh_token = create_refresh_token (identity=user[0]['username'])
            return {
                'message': 'Logged in as {}'.format (user[0]['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {
                'message': 'wrong credentials provided'
           }


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}