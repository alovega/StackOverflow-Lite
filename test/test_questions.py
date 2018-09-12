import unittest
import os
import json
from test.test_base import BaseTestCase


class TestQuestions(BaseTestCase):

    def test_post_question(self):
        signup = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res_signup = self.client.post("/auth/signup", json=signup)
        self.assertEqual(res_signup.status_code, 200)
        request = {"title":"question 1","description":"sample description"}
        res = self.client.post("/questions",json=request)
        self.assertEqual(res.status_code,201)

    def test_post_question_with_empty_title(self):
        request = {"title":"", "description": "this is a sample description"}
        res = self.client.post ("/questions", json=request)
        self.assertEqual (res.status_code, 400)
        self.assertIn("title can not be empty", str(res.json))

    def test_post_question_with_existing_title(self):
        request = {"title": "question5", "description": "this is a sample description"}
        res = self.client.post("/questions", json=request)
        res2 = self.client.post("/questions", json=request)
        self.assertEqual(res2.status_code, 409)



    def test_post_question_with_empty_description(self):
        request = {"title": "question 1", "description": ""}
        res = self.client.post ("/questions", json=request)
        self.assertEqual(res.json, {"message": "description can not be empty"})

    def test_post_question_with_empty_details(self):
        request = {"title": "", "description": ""}
        res = self.client.post("/questions", json=request)
        self.assertEqual(res.status_code, 400)

    def test_get_all_question(self):
        res = self.client.get("/questions")
        self.assertEqual(res.status_code, 200)


    def test_get_non_existing_question(self):
        res = self.client.get("/question/155")
        self.assertEqual(res.status_code, 404)


    def test_get_question(self):
        request = {"title": "question1", "description": "this is a sample description"}
        res1 = self.client.post("/questions", json=request)
        print (res1.json['question']['id'])
        res2 = self.client.get("/question/3")
        print (res2.json['question'])
        self.assertEqual(res1.json['question'], res2.json['question'])


    def test_post_answer(self):
        request = {"title": "question1", "description": "this is a sample description"}
        res1 = self.client.post("/questions", json=request)
        answer = {"answers": "sample answer2"}
        res4 = self.client.post("/answer/3", json=answer)
        print(res4)
        self.assertEqual(res4.status_code, 201)

    def test_post_empty_answer(self):
        request = {"title": "question1", "description": "this is a sample description"}
        res1 = self.client.post("/questions", json=request)
        answer = {"answers": ""}
        res4 = self.client.post("/answer/3", json=answer)
        print(res4)
        self.assertEqual(res4.status_code, 400)
        self.assertEqual(res4.json, {"message": "answer can not be empty"})




if __name__=='__main__':
    unittest.main()