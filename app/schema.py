import imp
from flask_marshmallow import  Marshmallow
from marshmallow import Schema, fields, validate

from app.models import Question, User
ma = Marshmallow()

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    badges = ma.auto_field()

class UserFormSchema(Schema):
    #below are the fields with the form should expect
    not_blank = validate.Length(min=2, error='Field cannot be blank')
    name = fields.Str(required=True, validate=not_blank)
    username = fields.Str(required=True, validate=not_blank)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=not_blank)

    class Meta:
        fields = ("email", "name", "username", "password")

class LoginSchema(Schema):
    #below are the fields with the form should expect
    not_blank = validate.Length(min=2, error='Field cannot be blank')
    username = fields.Str(required=True, validate=not_blank)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=not_blank)

    class Meta:
        fields = ("email", "name", "username", "password")

class QuestionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Question