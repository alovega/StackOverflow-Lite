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