import unittest
from test_base import BaseTestCase


class TestUserSignIn(BaseTestCase):
    """class for user sign in test case"""
    def test_user_login(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name": "kevin", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request_login = { "email": "alovegakevin@gmail.com", "password": "LUG4Z1V4"}
            res2 = self.client.post("/auth/login", json=request_login)
            self.assertEqual(res2.status_code, 202)

    def test_user_login_with_empty_details(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name":"Kelvin Alwa", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request_login = {"email": "", "password": ""}
            res2 = self.client.post("/auth/login", json=request_login)
            self.assertEqual(res2.status_code, 400)
            self.assertIn("email", str(res2.json))

    def test_user_login_with_empty_username(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name":"kelly", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request_login = {"email": "", "password": "12345TAHAH"}
            res2 = self.client.post("/auth/login", json=request_login)
            self.assertEqual(res2.status_code, 400)
            self.assertIn("email", str(res2.json))

    def test_login_with_empty_empty_password(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name":"kasuku", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request_login = {"email": "alovegakevin@gmail.com", "password": ""}
            res2 = self.client.post("/auth/login", json=request_login)
            self.assertEqual(res2.status_code, 400)
            self.assertIn("password", str(res2.json))

    def test_login_with_wrong_password(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa","name":"Kelvin", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request_login = {"email": "alovegakevin@gmail.com", "password": "123444"}
            res2 = self.client.post("/auth/login", json=request_login)
            self.assertEqual(res2.status_code, 401)
            self.assertIn("wrong credentials provided", str(res2.json))

    def test_login_with_wrong_email(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa","name":"kelvin","password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request_login = {"email": "alqwey@gmail.com", "password": "LuG$Z!V$"}
            res2 = self.client.post("/auth/login", json=request_login)
            self.assertEqual(res2.status_code, 404)
            self.assertIn("User doesn't exist", str(res2.json))


if __name__ == '__main__':
    unittest.main()
