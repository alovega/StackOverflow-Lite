import unittest
from models.test_base import BaseTestCase
import json


class TestUserDeleteQuestion(BaseTestCase):
    """test user can post a question"""

    def test_delete_question(self):
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
        #delete question
        delete = self.client.delete("/questions/1",
                                    headers = {"content-type":"application/json",
                                               "Authorization":token})
        self.assertEqual(delete.status_code,200)
        self.assertIn("successfully deleted", str(delete.json))


    def test_delete_question_that_does_not_exist(self):
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
        #delete question
        delete = self.client.delete("/questions/2",
                                    headers = {"content-type":"application/json",
                                               "Authorization":token})
        self.assertEqual(delete.status_code,404)
        self.assertIn("question doesn't exist", str(delete.json))


    def test_delete_question_you_did_not_post(self):
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
        request = {"email": "Timothy@gmail.com", "username": "Timo", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        # login user
        login2 = self.client.post(
            "/auth/login",
            data=json.dumps(dict(
                username="Timo",
                password="LUG4Z1V4"
            )),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 202)
        login2_data = json.loads(login2.data.decode())
        token2 = "Bearer" + " " + login2_data["access_token"]

        # post question
        Question = self.client.post(
            "/questions",
            data=json.dumps(dict(
                title="Question 2",
                details="Have they fixed your electricity",
            )),
            headers={"content-type": "application/json",
                     "Authorization": token2}
        )
        #delete question
        delete = self.client.delete("/questions/1",
                                    headers = {"content-type":"application/json",
                                               "Authorization":token2})
        self.assertEqual(delete.status_code,401)
        self.assertIn("you can't delete a question you didn't create", str(delete.json) )


if __name__== '__main__':
    unittest.main()
