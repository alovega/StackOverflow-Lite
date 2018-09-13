import unittest
from test.test_base import BaseTestCase
import json


class TestUserPostQuestion(BaseTestCase):
    """test user can post a question"""

    def test_post_question(self):
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


    def test_post_question_with_empty_parameters(self):
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
                title = "",
                details = "",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,400)
        self.assertIn("title can not be empty", str(Question.json))

    def test_post_question_with_empty_title(self):
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
                title = "",
                details = "Have you completed writing your API",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,400)
        self.assertIn("title can not be empty", str(Question.json))

    def test_post_question_with_empty_title(self):
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
                title = "",
                details = "Have you completed writing your API",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,400)
        self.assertIn("title can not be empty", str(Question.json))


    def test_post_question_with_empty_details(self):
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
                details = "",
            )),
            headers = {"content-type": "application/json",
                       "Authorization":token}
        )
        self.assertEqual(Question.status_code,400)
        self.assertIn("details can not be empty", str(Question.json))

    def test_post_an_existing_question(self):
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

        Question2 = self.client.post(
            "/questions",
            data=json.dumps(dict(
                title="Question 1",
                details="Have you completed writing your API",
            )),
            headers={"content-type": "application/json",
                     "Authorization": token}
        )
        self.assertEqual(Question2.status_code, 400)
        self.assertIn("title already used", str(Question2.json))


if __name__== '__main__':
    unittest.main()
