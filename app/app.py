from flask_restful import Resource, fields, reqparse, marshal, abort

from models.models import AppDb


AppDao = AppDb()


class QuestionDao(object):

    def __init__(self,question):
        self.question = question


class AnswerDao(object):
    def __init__(self,answer, id):
        self.answer = answer
        self.id = id


question_fields = {
    'question': fields.String,
    'answer': fields.String,
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('question', type=str, required=True, help='please input a question', location='json')
reqparse.remove_argument('answer')

reqparse_copy = reqparse.copy()
reqparse_copy.add_argument('answer', type=str, required=True, help='Can you input an answer', location='json')
reqparse_copy.add_argument('id',type=int, required=True, help='input the id of question you are answering', location='json')
reqparse_copy.remove_argument('question')

reqparse2_copy = reqparse.copy()
reqparse2_copy.add_argument('answer', type=str, required=True, help='Can you input an answer', location='json')
reqparse2_copy.add_argument('answer_id', type=int, required=True, help='input answer_id', location='json')
reqparse2_copy.remove_argument('question')

reqparse3_copy = reqparse.copy()
reqparse3_copy.remove_argument('answer',)
reqparse3_copy.add_argument('answer_id', type=int, required=True, help='input answer_id', location='json')
reqparse3_copy.remove_argument('question')


class QuestionList(Resource):

    def get(self):
        questions = AppDao.get_all_questions()

        return questions

    def post(self):

        args = reqparse.parse_args()

        questions = QuestionDao(question = args['question'])
        AppDao.insert_question(questions)
        return AppDao.insert_question(questions)


class Question(Resource):

    def get(self, id):
        questions = AppDao.get_question(id)

        if questions:
            return questions
        else:
            return {"message": "quest id not existing"}

    def delete(self, id):
        questions = AppDao.get_question(id)
        if questions:
            AppDao.delete_question(id)

        else:
            return {"message": "question id not existing"}


class AnswerList(Resource):

    def post(self,id):
        args = reqparse_copy.parse_args()
        answers = AnswerDao(answer=args['answer'],id=args['id'])
        AppDao.insert_answer(answers)


class Answers(Resource):

    def get(self):
        answer = AppDao.get_all_answers()

        return answer


class Answer(Resource):

    def put(self, id, answer_id):
        args = reqparse2_copy.parse_args()
        result = AppDao.update_answer(args['answer'],args['answer_id'])
        if result == -1:
            return {"message": "unable to edit this answer"}, 400
        if result:
            return AppDao.get_answers(args['answer_id'])
        else:
            abort(404)

class AcceptAnswer(Resource):
    def put(self,id, answer_id):
        result = AppDao.update_acceptance(answer_id)

        if result:
            return AppDao.get_all_answers()
        else:
            return {'message': 'request id given not existing'}, 400
