import json
import psycopg2
from psycopg2.extras import RealDictCursor


class AppDb:
    def __init__(self):
        try:
            self.connection = psycopg2.connect (host='localhost', dbname='app_database',
                                                user='postgres', password='LUG4Z1V4', port=5432)
        except:
            print("Unable to connect to the database")

    def getConnection(self):
        return self.connection

    def check_question_title_exists(self, title):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id,title,details, date from question where title = %(title)s ", {'title': title})
        rows = cur.fetchone()
        if rows:
            return True
        else:
            return False
        cur.close()

    def insert_question(self,QuestionDao):

        sql = """INSERT INTO question(title, details, date) VALUES (%s, %s, %s)"""
        cur = self.connection.cursor()
        cur.execute(sql, (QuestionDao.title, QuestionDao.details, QuestionDao.date,))
        cur.close()
        self.connection.commit()

    def check_answer_exists(self, answer):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT answer_id, answer from answer where answer = %(answer)s ", {'answer': answer})
        rows = cur.fetchone()
        if rows:
            return True
        else:
            return False
        cur.close()

    def insert_answer(self, AnswerDao):

        sql = """INSERT INTO answer(answer, question_id) VALUES (%s, %s)"""
        cur = self.connection.cursor()
        cur.execute(sql, (AnswerDao.answer,AnswerDao.id))
        self.connection.commit()
        cur.close()

    def get_all_questions(self):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id,title,details,date from question")
        rows = cur.fetchall()
        return rows

    def get_all_answers(self):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT answer_id,answer,id  from answer")
        rows = cur.fetchall()
        return rows


    def get_question_with_answers(self, id):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(""" SELECT id,title, details from question where id = %(id)s""", {'id': id})
        question_row = cur.fetchall()
        cur.execute("""SELECT  answer_id, answer, preferred from answer INNER JOIN question ON (answer.question_id = question.id) 
        where question_id = %(id)s """,
                    {'id': id})
        rows = cur.fetchall()

        if rows:
            question = (question_row, rows)
            return list(question)
        else:
            question1 = (question_row, {"answer":"be the first to answer"})
            return list(question1)


    def get_answers(self, answer_id):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT answer_id, answer from answer where answer_id = %(id)s""",
                    {'id': answer_id})
        rows = cur.fetchall()
        return rows


    def delete_question(self,id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE from question where id = %(id)s ", {'id': id})
        rows_deleted = cur.rowcount
        self.connection.commit()
        print(json.dumps(rows_deleted, indent=2))
        cur = self.connection.cursor(cursor_factory=RealDictCursor)

    def update_answer(self, answer, answer_id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE answer set answer = '{0}' where answer_id = '{1}' ".format(answer, answer_id)
        cur.execute(sql)
        print (cur)
        updated_rows = cur.rowcount
        self.connection.commit()
        cur.close()
        return updated_rows

    def update_acceptance(self,answer_id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE preferred set preferred = true  where id = {0}".format(answer_id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        print(json.dumps(updated_rows, indent=2))
        self.connection.commit()
        cur.close()
        return updated_rows

    def insert_user(self, UserApi):
        sql = """INSERT INTO users(email, username, password) 
          VALUES (%s,%s,%s)"""
        # get connection
        cur = self.connection.cursor()
        # insert into database
        cur.execute(sql, (UserApi.email, UserApi.username, UserApi.password,))
        self.connection.commit()
        cur.close()

    def get_user_by_username(self, username):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT email,username,password from users 
                        where username = %(username)s """,
                    {'username': username})
        rows = cur.fetchall()
        return rows

    def get_all(self):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, email, username,password  from users")
        rows = cur.fetchall()
        return rows

    def check_user_exist_by_username(self, username):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, username, password from users where username = %(username)s", {'username':
                                                                                                   username})
        rows = cur.fetchone()
        if rows:
            return True
        else:
            return False
        cur.close()

    def check_user_exist_by_email(self, email):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, username, password from users where email = %(email)s", {'email':
                                                                                                   email})
        rows = cur.fetchone()
        if rows:
            return True
        else:
            return False
        cur.close()