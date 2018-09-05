
from flask_restful import Resource, reqparse, abort
import datetime
from flask_restful import fields
import json

questions = [    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'answers': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'answers': [{'id':1,
                      'answer':'False'}]
    }]


class QuestionDao(object):
    def __init__(self,id,title, description, date, answers):
        self.id = id
        self.title = title
        self.description = description
        self.date = datetime.datetime.now()
        self.answers = answers


question_fields = {
    'title': fields.String,
    'description': fields.String,
    'date':fields.datetime,
    'answers': fields.String
}


class Questions(Resource):

    def get(self):
        return {'qestions': questions}