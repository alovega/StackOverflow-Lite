
from flask_restful import Resource, reqparse, abort
import datetime
from flask_restful import fields
import json

questions = [{
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
answers = []


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

reqparse = reqparse.RequestParser()
reqparse.add_argument('title', type=str, required=True, help='No request title provided', location='json')
reqparse.add_argument('description', type=str, required=True, help='No request description provided', location='json')
reqparse_copy = reqparse.copy()
reqparse_copy.add_argument('answer', type=str, required=True, help='plase provide your answer', location='json')
reqparse_copy.remove_argument('title')
reqparse_copy.remove_argument('description')


class Questions(Resource):

    def get(self):
        return {'qestions': questions}


class Answer(Resource):

    def post(self, id):
        args = reqparse_copy.parse_args()
        for question in questions:
            if question['id'] == id:
                answers = {
                    'id': question['answers'][-1]['id'] + 1,
                    'answer': args['answer'],
                }
                question['answers'].append(answers)

                return {'answers': answers}, 201


