from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.models import DatabaseModel

AppDao = DatabaseModel()

DTime = datetime.now()


class QuestionDao(object):

    def __init__(self,title, details, author):
        self.title = title
        self.details = details
        self.date = str(DTime.date())
        self.author = author


class AnswerDao(object):

    def __init__(self,answer,id,author):
        self.answer = answer
        self.id = id
        self.author = author


class Questions(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('details', type=str, location='json')
        super(Questions, self).__init__()
    @jwt_required
    def get(self):
        questions = AppDao.get_all_questions()
        if questions:
            return questions
        return {"message":"no questions posted"}

        return questions
    @jwt_required
    def post(self):
        name = get_jwt_identity ()
        args = self.reqparse.parse_args()
        title = args['title']
        details = args['details']
        author = name

        if not title.replace(" ", ""):
            return {"message":"title can not be empty"}, 400
        elif not details.replace(" ", ""):
            return {"message":"details can not be empty"}, 400

        questions = QuestionDao(title = title, details= details, author = author)
        if AppDao.check_question_title_exists(questions.title):
            return {"message": "title already used"}, 400

        AppDao.insert_question(questions)
        return {questions.title: questions.details}


class Question(Resource):
    @jwt_required
    def get(self, id):
        questions = AppDao.get_question_with_answers(id)
        print(questions)
        if questions[0]:
            return questions
        return {"message":"question does not exist"},404

    @jwt_required
    def delete(self, id):
        user = get_jwt_identity()
        questions = AppDao.get_question_with_answers(id)
        if questions[0]:
            if questions[0][0]['author'] == user:
                AppDao.delete_question(id)
                return{"message":"successfully deleted"},200

            return {"message": "you can't delete a question you didn't create"}, 401

        elif not questions[0]:
            return {"message":"questions doesn't exists"}


class Answers(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, location='json')
        self.reqparse.add_argument('id', type=int, location='json')
        super(Answers, self).__init__()
    @jwt_required
    def post(self, id):
        name = get_jwt_identity()
        args = self.reqparse.parse_args()
        answer = args['answer']
        author = name
        if not answer.replace(" ", ""):
            return {"message":"can't post an empty answer"}, 400
        answers = AnswerDao(answer=answer, id=id, author = author)
        print(answers)
        questions = AppDao.get_question(id)

        if questions:
            if AppDao.check_answer_exists(answers.answer):
                return {"message": "answer already posted"}, 400
            AppDao.insert_answer(answers)
            return {"answer": answers.answer}
        return {"message":"can post to a question that doesn't exist"}


class Answer(Resource):


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, location='json')
        self.reqparse.add_argument('id', type=str, location='json')
        super(Answer, self).__init__()
    @jwt_required
    def put(self, id,answer_id):
        name = get_jwt_identity()
        args = self.reqparse.parse_args()
        answer = args['answer']
        if not answer.replace(" ", ""):
            return {"message":"can't post an empty answer"}, 400
        answers = AnswerDao(answer=answer, id=id, author= name)
        print(answers)
        check = AppDao.get_answers(answer_id)
        question_author = AppDao.get_question_with_answers(id)
        print(check)
        if check[0]['user_name'] == name:
            if check:
                if AppDao.check_answer_exists(answers.answer):
                    return {"message": "answer already posted"}, 400
                AppDao.update_answer(answers.answer, answer_id)
                return {"update":answers.answer}

            return {"answer does not exist"},404
        if question_author[0][0]['author'] == name:
            AppDao.update_preferred(answer_id)
            return {"message":"answer {0} is now preferred".format(answer_id)},201

        return {"message":"you are not authorized to update the answer"},401


