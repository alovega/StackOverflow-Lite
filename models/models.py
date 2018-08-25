import json
import psycopg2
from psycopg2.extras import RealDictCursor

class AppDb:
    def __init__(self):
        try:
            self.connection = psycopg2.connect (host='localhost', dbname='app_database', user='postgres', password='LUG4Z1V4', port=5432)
        except:
            print("Unable to connect to the database")

    def getConnection(self):
        return self.connection

    def insert_question(self,QuestionDao):
        sql = """INSERT INTO question(question) VALUES (%s)"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (QuestionDao.question,))
        self.connection.commit()
        result = cur.fetchone()
        cur.close()
        return result

    def insert_answer(self, AnswerDao):

        sql = """INSERT INTO answer(answer, id) VALUES (%s, %s)"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (AnswerDao.answer, AnswerDao.id))
        self.connection.commit()
        result = cur.fetchone()[0]
        cur.close()
        return result

    def get_all_questions(self):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id,question  from question")
        rows = cur.fetchall()
        return rows

    def get_all_answers(self):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT answer_id,answer,id  from answer")
        rows = cur.fetchall()
        return rows

    def get_question(self, id):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT id,question from question 
                              where id = %(id)s """,
                    {'id': id})
        rows = cur.fetchall()
        return rows

    def get_answers(self, id):

        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT answer_id, answer from answer where id = %(id)s""",
                    {'id': id})
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
        acceptance = "select accept  from answer where answer_id = {0}".format(answer_id)
        cur.execute(acceptance)
        approved = cur.fetchone()
        print (approved)
        if approved['accept']:
            cur.close()
            return -1

        sql = "UPDATE answer set answer = '{0}' ".format(answer)
        cur.execute(sql)
        updated_rows = cur.rowcount
        self.connection.commit()
        cur.close()
        return updated_rows

    def update_acceptance(self,answer_id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE accept set accept = true  where id = {0}".format(answer_id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        print(json.dumps(updated_rows, indent=2))
        self.connection.commit()
        cur.close()
        return updated_rows