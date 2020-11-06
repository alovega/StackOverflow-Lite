import unittest
from models.test_base import BaseTestCase
import json


class TestUserGetQuestion(BaseTestCase):
    """test user can post a question"""

    def test_get_a_question(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        # login user
        login = self.client.post(
            "/auth/login",
            data = json.dumps(dict(
                username = "alwa",
                password = "LUG4Z1V4"
            )),
            headers = {"content-type": "application/json"}
        )
        self.assertEqual(login.status_code,202)
        login_data = json.loads(login.data.decode())
        token = "Bearer" +" " +login_data["access_token"]

        # post question
        Question = self.client.post(
            "/questions",
            data = json.dumps(dict(
                title = "Question 1",
                details = "Have you completed writing your API",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,201)
        #get one question
        response = self.client.get("/questions/1",
                                   headers = {"content-type": "application/json",
                                              "Authorization":token})
        self.assertEqual(response.status_code,200)

    def test_get_all_question(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        # login user
        login = self.client.post(
            "/auth/login",
            data = json.dumps(dict(
                username = "alwa",
                password = "LUG4Z1V4"
            )),
            headers = {"content-type": "application/json"}
        )
        self.assertEqual(login.status_code,202)
        login_data = json.loads(login.data.decode())
        token = "Bearer" +" " +login_data["access_token"]

        # post question
        Question = self.client.post(
            "/questions",
            data = json.dumps(dict(
                title = "Question 1",
                details = "Have you completed writing your API",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,201)
        #get one question
        response = self.client.get("/questions",
                                   headers = {"content-type": "application/json",
                                              "Authorization":token})
        self.assertEqual(response.status_code,200)

    def test_get_a_question_that_does_not_exist(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        # login user
        login = self.client.post(
            "/auth/login",
            data = json.dumps(dict(
                username = "alwa",
                password = "LUG4Z1V4"
            )),
            headers = {"content-type": "application/json"}
        )
        self.assertEqual(login.status_code,202)
        login_data = json.loads(login.data.decode())
        token = "Bearer" +" " +login_data["access_token"]

        # post question
        Question = self.client.post(
            "/questions",
            data = json.dumps(dict(
                title = "Question 1",
                details = "Have you completed writing your API",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,201)
        #get a question that doen't exist
        response = self.client.get("/questions/2",
                                   headers = {"content-type": "application/json",
                                              "Authorization":token})
        self.assertEqual(response.status_code,404)
        self.assertIn("question does not exist", str(response.json))


if __name__== '__main__':
    unittest.main()
