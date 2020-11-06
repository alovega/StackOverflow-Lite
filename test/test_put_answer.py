import unittest
from models.test_base import BaseTestCase
import json


class TestUserUpdateAnswers(BaseTestCase):
    """test user can post a question"""

    def test_update_answer(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        # login user
        login = self.client.post(
            "/auth/login",
            data=json.dumps(dict(
                username="alwa",
                password="LUG4Z1V4"
            )),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 202)
        login_data = json.loads(login.data.decode())
        token = "Bearer" + " " + login_data["access_token"]

        # post question
        Question = self.client.post(
            "/questions",
            data=json.dumps(dict(
                title="Question 1",
                details="Have you completed writing your API",
            )),
            headers={"content-type": "application/json",
                     "Authorization": token}
        )
        self.assertEqual(Question.status_code, 201)

        # post answer
        Answer = self.client.post(
            "/questions/1/answers",
            data=json.dumps(dict(
                answer="This is my sample answer",
            )),
            headers={"content-type": "application/json",
                     "Authorization": token}
        )
        self.assertEqual(Answer.status_code, 201)
        # Update answer
        new_Answer= self.client.put(
            "/questions/1/answers/1",
            data=json.dumps(dict(
                answer="This is my new answer",
            )),
            headers={"content-type": "application/json",
                     "Authorization": token}
        )
        self.assertEqual(new_Answer.status_code, 201)

        def test_update_answer(self):
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            # login user
            login = self.client.post(
                "/auth/login",
                data=json.dumps(dict(
                    username="alwa",
                    password="LUG4Z1V4"
                )),
                headers={"content-type": "application/json"}
            )
            self.assertEqual(login.status_code, 202)
            login_data = json.loads(login.data.decode())
            token = "Bearer" + " " + login_data["access_token"]

            # post question
            Question = self.client.post(
                "/questions",
                data=json.dumps(dict(
                    title="Question 1",
                    details="Have you completed writing your API",
                )),
                headers={"content-type": "application/json",
                         "Authorization": token}
            )
            self.assertEqual(Question.status_code, 201)

            # post answer
            Answer = self.client.post(
                "/questions/1/answers",
                data=json.dumps(dict(
                    answer="This is my sample answer",
                )),
                headers={"content-type": "application/json",
                         "Authorization": token}
            )
            self.assertEqual(Answer.status_code, 201)
            # Update answer
            new_Answer = self.client.put(
                "/questions/1/answers/1",
                data=json.dumps(dict(
                    answer="This is my new answer",
                )),
                headers={"content-type": "application/json",
                         "Authorization": token}
            )
            self.assertEqual(new_Answer.status_code, 201)


if __name__ == '__main__':
    unittest.main()
