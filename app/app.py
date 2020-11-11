from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.models import DatabaseModel, insert_question

AppDao = DatabaseModel()

DTime = datetime.now()


class QuestionDao(object):

    def __init__(self, title, details, author):
        self.title = title
        self.details = details
        self.date = str(DTime.date())
        self.author = author


class AnswerDao(object):

    def __init__(self, answer, id, author):
        self.answer = answer
        self.id = id
        self.author = author


class Questions(Resource):

    def __init__(self):
        self.request_parse = reqparse.RequestParser()
        self.request_parse.add_argument('title', type=str, location=['json', 'form'])
        self.request_parse.add_argument('details', type=str, location=['json', 'form'])
        super(Questions, self).__init__()

    @jwt_required
    def get(self):
        """
                view all questions
                ---
                tags:
                    - Questions
                description: Questions posted by users
                security:
                    - TokenHeader: []
                parameters:
                    - name: Question
                      in: path
                      description: Questions posted
                      schema:
                        $ref: '#/definitions/Post_question'
                responses:
                    200:
                        description: all posted questions
                        schema:
                            $ref: '#/definitions/Post_question'
                    404:
                        description: no questions posted, sorry
                """

        questions = AppDao.get_all_questions()
        if questions:
            return questions, 200
        return {"message": "no questions posted"}, 404

    @jwt_required
    def post(self):
        """
               create a question
               ---
               tags:
                   - Question
               description: users post questions
               security:
                   - TokenHeader: []
               parameters:
                   - name: Question
                     in: body
                     schema:
                       $ref: '#/definitions/Post_question'
               responses:
                   200:
                       description: question created
                   400:
                       description: Bad request
               """
        name = get_jwt_identity()
        args = self.request_parse.parse_args()
        title = args['title']
        details = args['details']
        author = name

        if not title.replace(" ", ""):
            return {"message": "title can not be empty"}, 400
        elif not details.replace(" ", ""):
            return {"message": "details can not be empty"}, 400

        questions = QuestionDao(title=title, details=details, author=author)
        if AppDao.check_question_title_exists(questions.title):
            return {"message": "title already used"}, 400

        insert_question(questions)
        return {questions.title: questions.details}, 201


class Question(Resource):
    @jwt_required
    def get(self, id):
        """
               View a question
               ---
               tags:
                   - Question
               description: A single question with all its answers returned
               security:
                   - TokenHeader: []
               parameters:
                   - name: id
                     in: path
                     type : integer
                     format: int64
                     minimum: 1
                     description: question id
               responses:
                   200:
                       description: a question and all its answers
                       schema:
                           $ref: '#/definitions/Post_question'
                   404:
                       description: Question does not exist
                   200:
                       description: a question and its answers
               """
        questions = AppDao.get_question_with_answers(id)
        print(questions)
        if questions[0]:
            return questions, 200
        return {"message": "question does not exist"}, 404

    @jwt_required
    def delete(self, id):
        """
                delete a question
                ---
                tags:
                    - Question
                security:
                    - TokenHeader: []
                parameters:
                    - name: id
                      in: path
                      type : integer
                      format: int64
                      minimum: 1
                      description: Question id
                schema:
                    $ref: '#/definitions/Post_question'
                responses:
                    200:
                        description: successfully deleted

                """
        user = get_jwt_identity()
        questions = AppDao.get_question_with_answers(id)
        if questions[0]:
            if questions[0][0]['author'] == user:
                AppDao.delete_question(id)
                return {"message": "successfully deleted"}, 200

            return {"message": "you can't delete a question you didn't create"}, 401

        elif not questions[0]:
            return {"message": "question doesn't exists"}, 404


class Answers(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, location=['json', 'form'])
        self.reqparse.add_argument('id', type=int, location=['json', 'form'])
        super(Answers, self).__init__()

    @jwt_required
    def post(self, id):
        """
                post an answer to a question
                ---
                tags:
                    - Answers
                security:
                    - TokenHeader: []
                parameters:
                    - name: id
                      in: path
                      description: answer_id
                      schema:
                        $ref: '#/definitions/Answers'
                responses:
                    201:
                        description: Answer has been created
                    400:
                        description: bad request
                    404:
                        description: can't post an answer to a question that doesn't exist
                """
        name = get_jwt_identity()
        args = self.reqparse.parse_args()
        answer = args['answer']
        author = name
        if not answer.replace(" ", ""):
            return {"message": "can't post an empty answer"}, 400
        answers = AnswerDao(answer=answer, id=id, author=author)
        questions = AppDao.get_question(id)

        if questions:
            if AppDao.check_answer_exists(answers.answer):
                return {"message": "answer already posted"}, 400
            AppDao.insert_answer(answers)
            return {"answer": answers.answer}, 201
        return {"message": "can post to a question that doesn't exist"}, 404


class Answer(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, location=['json', 'form'])
        self.reqparse.add_argument('id', type=str, location=['json', 'form'])
        super(Answer, self).__init__()

    @jwt_required
    def put(self, id, answer_id):
        """
                Update Answer
                ---
                tags:
                    - Answer status
                description: Update the status of an answer
                security:
                    - TokenHeader: []
                parameters:
                    - name:question_id
                      in: path
                      type : integer
                      format: int64
                      minimum: 1
                      description: Question to update
                    - name: Answer_id
                      in: path
                      type : integer
                      format: int64
                      minimum: 1
                      description: Answer id to the question you are updating
                    - name: status
                      in: body
                      schema:
                        $ref: '#/definitions/Answers'

                responses:
                    201:
                        description: Answer updated successfully
                    401:
                        description:  users cannot accept  answers to questions they didn't ask
                    400:
                        description: Bad request
                """

        name = get_jwt_identity()
        args = self.reqparse.parse_args()
        answer = args['answer']
        if not answer.replace(" ", ""):
            return {"message": "can't post an empty answer"}, 400
        answers = AnswerDao(answer=answer, id=id, author=name)

        check = AppDao.get_answers(answer_id)
        print(check)

        question_author = AppDao.get_question_with_answers(id)

        if check:
            if check[0]['user_name'] == name:
                if AppDao.check_answer_exists(answers.answer):
                    return {"message": "answer already posted"}, 400
                AppDao.update_answer(answers.answer, id)
                return {"update": answers.answer}, 201
        if not check:
            return {"message": "no such answer"}

        if question_author[0][0]['author'] == name:
            if AppDao.check_answer_exists(answers.answer):
                AppDao.update_preferred(answer_id)
                return {"message": "answer {0} is now preferred".format(answer_id)}, 200
            return {"message": "answer does not exist"}

        return {"message": "you are not authorized to update the answer"}, 401
