from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.models import AppDb


AppDao = AppDb()

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
            return {"message": "title already used"}, 202

        AppDao.insert_question(questions)
        return {questions.title: questions.details}


class Question(Resource):
    @jwt_required
    def get(self, id):
        questions = AppDao.get_question_with_answers(id)
        print(questions)

        if questions:
            return questions

    @jwt_required
    def delete(self, id):
        user = get_jwt_identity()
        questions = AppDao.get_question_with_answers(id)
        if questions[0][0]['author'] == user:
            if questions:
                AppDao.delete_question(id)
                return{"message":"successfully deleted"}

            else:
                return {"message": "question id not existing"}
        return {"message":"you can't delete a question you didn't create"}

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
        if AppDao.check_answer_exists(answers.answer):
            return {"message": "answer already posted"}, 400
        AppDao.insert_answer(answers)
        return {"answer": answers.answer}

    @jwt_required
    def get(self):
        answer = AppDao.get_all_answers()

        return answer


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
                result =AppDao.update_answer(answers.answer, answer_id)
                return result

            return {"answer does not exist"}
        elif question_author[0][0]['author'] == name:
            result = AppDao.update_preferred(answer_id)
            return  result
        return {"message":"you are not authorized to update question"}


