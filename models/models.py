import json
from models.db import db


class DatabaseModel():

    def check_question_title_exists(self, title):
        #cur = self.connection.cursor(cursor_factory=RealDictCursor)
        db.cursor.execute("SELECT id,title,details, date from question where title = %(title)s ", {'title': title})
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    def insert_question(self,QuestionDao):

        sql = """INSERT INTO question(title, details, date, author) VALUES (%s, %s, %s, %s)"""
        db.cursor.execute(sql, (QuestionDao.title, QuestionDao.details, QuestionDao.date, QuestionDao.author))
        db.commit()

    def check_answer_exists(self, answer):
        db.cursor.execute("SELECT answer_id, answer from answer where answer = %(answer)s ", {'answer': answer})
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    def insert_answer(self, AnswerDao):

        sql = """INSERT INTO answer(answer, question_id, user_name) VALUES (%s, %s, %s)"""
        db.cursor.execute(sql, (AnswerDao.answer,AnswerDao.id, AnswerDao.author))
        db.commit()

    def get_all_questions(self):

        db.cursor.execute("SELECT id,title,details,date from question")
        rows = db.cursor.fetchall()
        return rows

    def get_all_answers(self):

        db.cursor.execute("SELECT answer_id,answer,id  from answer")
        rows = db.cursor.fetchall()
        return rows

    def get_question_with_answers(self, id):
        db.cursor.execute(""" SELECT id,title, details, date, author from question where id = %(id)s""", {'id': id})
        question_row = db.cursor.fetchall()
        db.cursor.execute("""SELECT  answer_id, answer, preferred, question_id, user_name from answer INNER JOIN question ON (answer.question_id = question.id) 
        where question_id = %(id)s """,
                    {'id': id})
        rows = db.cursor.fetchall()
        if rows:
            question = (question_row, rows)
            return list(question)
        else:
            question1 = (question_row, {"answer":"be the first to answer"})
            return list(question1)

    def get_answers(self, answer_id):
        db.cursor.execute("""SELECT answer_id, answer, user_name from answer where answer_id = %(id)s""",
                    {'id': answer_id})
        rows = db.cursor.fetchall()
        return rows

    def get_question(self, id):
        db.cursor.execute("""SELECT id, title, details from question where id = %(id)s""",
                    {'id': id})
        rows = db.cursor.fetchall()
        return rows

    def delete_question(self,id):
        db.cursor.execute("DELETE from question where id = %(id)s ", {'id': id})
        rows_deleted = db.cursor.rowcount
        db.commit()
        print(json.dumps(rows_deleted, indent=2))

    def update_answer(self, answer, answer_id):
        sql = "UPDATE answer set answer = '{0}' where answer_id = '{1}' ".format(answer, answer_id)
        db.cursor.execute(sql)
        print (db.cursor.execute(sql))
        updated_rows = db.cursor.rowcount
        db.commit()
        return updated_rows

    def update_preferred(self,answer_id):
        sql = "UPDATE answer set preferred = true  where answer_id = {0}".format(answer_id)
        db.cursor.execute(sql)
        updated_rows = db.cursor.rowcount
        print(json.dumps(updated_rows, indent=2))
        db.commit()
        return updated_rows

    def insert_user(self, UserApi):
        sql = """INSERT INTO users(email, username, password) 
          VALUES (%s,%s,%s)"""
        # insert into database
        db.cursor.execute(sql, (UserApi.email, UserApi.username, UserApi.password))
        db.commit()


    def get_user_by_username(self, username):
        db.cursor.execute("""SELECT email,username,password from users 
                        where username = %(username)s """,
                    {'username': username})
        rows = db.cursor.fetchall()
        return rows

    def get_all(self):
        db.cursor.execute("SELECT id, email, username,password  from users")
        rows = db.cursor.fetchall()
        return rows

    def check_user_exist_by_username(self, username):
        db.cursor.execute("SELECT id, username, password from users where username = %(username)s", {'username':
                                                                                                   username})
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    def check_user_exist_by_email(self, email):
        db.cursor.execute("SELECT id, username, password from users where email = %(email)s", {'email':
                                                                                                   email})
        rows = db.cursor.fetchone()
        if rows:
            return True
        else:
            return False

    def drop_table(self, table_name):
        db.cursor.execute("DROP TABLE IF EXISTS" + " "+ table_name +";")
        db.commit()