import datetime
import json
from flask_restful import Resource, reqparse


questions = [{
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
    }]

answers = []


class Questions(Resource):
    """class representing the resource endpoints for getting all questions and posting  a question"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(Questions, self).__init__()

    # this method converts the datetime object to a string
    def myconverter(self,o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def get(self):
        return {'qestions': questions}

    def post(self):
        date = datetime.datetime.now()
        args = self.reqparse.parse_args()
        question = {
            'id': questions[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'date': json.dumps(date, default=self.myconverter),
        }
        if not question['title'].replace(" ", ""):
            return {"message": "title can not be empty"},400
        elif not question['description'].replace(" ", ""):
            return {"message": "description can not be empty"},400

        for i in questions:
            if i['title'] == args['title']:
                return{"message": "title already used"},409
        questions.append(question)
        print(question)
        return {'question': question},201


class Question(Resource):
    """this class represents the resource endpoint for getting a single question"""
    def get(self, id):
        question = [question for question in questions if question['id'] == id]
        if len(question) == 0:
            return {'message':'question does not exist'},404
        return {'question': question[0]}


class Answer(Resource):
    """this class represents the resource endpoint for posting an answer to a question"""
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answers', type=str, location='json')
        super(Answer, self).__init__()

    def post(self, id):
        args = self.reqparse.parse_args()
        question = [question for question in questions if question['id'] == id]
        if len(question) == 0:
            return {"message": "question does not exist"},400
        else:
            answer = {
                'id': id,
                'answers': args['answers']
            }
            if not answer['answers'].replace(" ", ""):
                return {"message": "answer can not be empty"},400
            answers.append(answer)
            print(answer)
            return {'answer': answer}, 201


class HelloWorld(Resource):
    def post(self):
        return {"hello":"world"}



