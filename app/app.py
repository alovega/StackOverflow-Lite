from flask_restful import Resource, reqparse, abort
import datetime
import json

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

class QuestionDao(object):
    """class representing the questions object"""
    def __init__(self,id,title, description):
        self.id = id
        self.title = title
        self.description = description
        self.date = datetime.datetime.now()


class AnswerDao(object):
    """class representing the answer object"""
    def __init__(self, id, answer):
        self.id = id
        self.answer = answer

"""this indicates the arguments that we will be passing while using our Api endpoints"""

reqparse = reqparse.RequestParser()
reqparse.add_argument('title', type=str, required=True, help='title can not be empty', location='json')
reqparse.add_argument('description', type=str, required=True, help='description can not be empty', location='json')
reqparse.add_argument('answers', action='append', location='json')
reqparse_copy = reqparse.copy()
reqparse_copy.add_argument('answers', type=str, required=True, help='Answer can not be empty', location='json')
reqparse_copy.remove_argument('title')
reqparse_copy.remove_argument('description')

#this method converts the datetime object to a string
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class Questions(Resource):
    """class representing the resource endpoints for getting all questions and posting  a question"""

    def get(self):
        return {'qestions': questions}

    def post(self):
        date = datetime.datetime.now()
        args = reqparse.parse_args()
        question = {
            'id': questions[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'date': json.dumps(date, default=myconverter),
        }
        if not question['title'].replace(" ", ""):
            return {"message": "title can not be empty"}
        elif not question['description'].replace(" ", ""):
            return {"message": "description can not be empty"}
        else:
            questions.append(question)
            print(question)
            return {'question': question}, 201


class Question(Resource):
    """this class represents the resource endpoint for getting a single question"""
    def get(self, id):
        question = [question for question in questions if question['id'] == id]
        if len(question) == 0:
            abort(404)
        return {'question': question[0]}


class Answer(Resource):
    """this class represents the resource endpoint for posting an answer to a question"""
    def post(self, id):
        args = reqparse_copy.parse_args()
        for question in questions:
            if question['id'] == id:

                answer = {
                    'id': id,
                    'answers': args['answers']
                }
                if not answer['answers'].replace(" ", ""):
                    return {"message": "answer can not be empty"}
                answers.append(answer)
                print(answer)
        return {'answers': answers}, 201



