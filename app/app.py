from flask_restful import Resource, fields, reqparse, marshal, abort

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

question_fields = {
    'title': fields.String,
    'description': fields.String,
    'answers': fields.String
}


class QuestionList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(QuestionList, self).__init__()

    def get(self):
        return {'qestions': questions}

    def post(self):
        args = self.reqparse.parse_args()
        question = {
            'id': questions[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
        }

        questions.append(question)
        return {'question': questions}, 201




class Question(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(Question, self).__init__()

    def get(self, id):
        question = [question for question in questions if question['id'] == id]
        if len(questions) == 0:
            abort(404)
        return {'question':question[0]}


    def delete(self, id):
        question = [question for question in questions if question['id'] == id]
        if len(question) == 0:
            abort(404)
        questions.remove(question[0])
        return {'questions': questions}


class Answer(Question, Resource):
    answers = []

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answers', type=str, location='json')
        super(Answer, self).__init__()

    def post(self, id):
        question = [question for question in questions if question['id'] == id]
        if len(question) == 0:
            abort(404)
        else:
            args = self.reqparse.parse_args()
            self.answer = {
                'id':self.answers[-1]['id'] + 1,
                'answer':args['answers'],
            }
            self.answers.append(self.answer)
        return {'question': question}

    def put(self, id):
        question = [question for question in questions if question['id'] == id]
        if len(question) == 0:
            abort(404)
        question = question[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            for answer in v:
                if len(v) == 0:
                    abort(404)
        return {'question': question}
