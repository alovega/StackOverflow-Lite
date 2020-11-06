import json
from models.db import db


def insert_question(QuestionDao):
    sql = """INSERT INTO question(title, details, date, author) VALUES (%s, %s, %s, %s)"""
    db.cursor.execute(sql, (QuestionDao.title, QuestionDao.details, QuestionDao.date, QuestionDao.author))
    db.commit()


class DatabaseModel:

    @staticmethod
    def check_question_title_exists(title):
        db.cursor.execute(
            "SELECT id,title,details, date from question where title = %(title)s ", {'title': title}
        )
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    @staticmethod
    def check_answer_exists(answer):
        db.cursor.execute("SELECT answer_id, answer from answer where answer = %(answer)s ", {'answer': answer})
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    @staticmethod
    def insert_answer(AnswerDao):

        sql = """INSERT INTO answer(answer, question_id, user_name) VALUES (%s, %s, %s)"""
        db.cursor.execute(sql, (AnswerDao.answer, AnswerDao.id, AnswerDao.author))
        db.commit()

    @staticmethod
    def get_all_questions():

        db.cursor.execute("SELECT id,title,details,date from question")
        rows = db.cursor.fetchall()
        return rows

    @staticmethod
    def get_all_answers():

        db.cursor.execute("SELECT answer_id,answer,id  from answer")
        rows = db.cursor.fetchall()
        return rows

    @staticmethod
    def get_question_with_answers(id):
        db.cursor.execute(
            """ SELECT id,title, details, date, author from question where id = %(id)s""", {'id': id}
        )
        question_row = db.cursor.fetchall()
        db.cursor.execute(
            """SELECT  answer_id, answer, preferred, question_id, user_name from answer INNER JOIN question ON (
            answer.question_id = question.id) where question_id = %(id)s """,
            {'id': id})
        rows = db.cursor.fetchall()
        if rows:
            question = (question_row, rows)
            return list(question)
        else:
            question1 = (question_row, {"answer": "be the first to answer"})
            return list(question1)

    @staticmethod
    def get_answers(answer_id):
        db.cursor.execute("""SELECT answer_id, answer, user_name from answer where answer_id = %(id)s""",
                          {'id': answer_id})
        rows = db.cursor.fetchall()
        return rows

    @staticmethod
    def get_question(id):
        db.cursor.execute("""SELECT id, title, details from question where id = %(id)s""",
                          {'id': id})
        rows = db.cursor.fetchall()
        return rows

    @staticmethod
    def delete_question(id):
        db.cursor.execute("DELETE from question where id = %(id)s ", {'id': id})
        rows_deleted = db.cursor.rowcount
        db.commit()
        print(json.dumps(rows_deleted, indent=2))

    @staticmethod
    def update_answer(answer, answer_id):
        sql = "UPDATE answer set answer = '{0}' where answer_id = '{1}' ".format(answer, answer_id)
        db.cursor.execute(sql)
        print(db.cursor.execute(sql))
        updated_rows = db.cursor.rowcount
        db.commit()
        return updated_rows

    @staticmethod
    def update_preferred(answer_id):
        sql = "UPDATE answer set preferred = true  where answer_id = {0}".format(answer_id)
        db.cursor.execute(sql)
        updated_rows = db.cursor.rowcount
        print(json.dumps(updated_rows, indent=2))
        db.commit()
        return updated_rows

    @staticmethod
    def insert_user(UserApi):
        sql = """INSERT INTO users(email, username, password) 
          VALUES (%s,%s,%s)"""
        # insert into database
        db.cursor.execute(sql, (UserApi.email, UserApi.username, UserApi.password))
        db.commit()

    @staticmethod
    def get_user_by_username(username):
        db.cursor.execute("""SELECT email,username,password from users 
                        where username = %(username)s """,
                          {'username': username})
        rows = db.cursor.fetchall()
        return rows

    @staticmethod
    def get_all():
        db.cursor.execute("SELECT id, email, username,password  from users")
        rows = db.cursor.fetchall()
        return rows

    @staticmethod
    def check_user_exist_by_username(username):
        db.cursor.execute(
            "SELECT id, username, password from users where username = %(username)s", {'username': username}
        )
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    @staticmethod
    def check_user_exist_by_email(email):
        db.cursor.execute(
            "SELECT id, username, password from users where email = %(email)s", {'email': email}
        )
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    @staticmethod
    def drop_table(table_name):
        db.cursor.execute("DROP TABLE IF EXISTS" + " " + table_name + ";")
        db.commit()
