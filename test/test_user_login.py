import unittest
from models.test_base import BaseTestCase


class TestUserSignIn(BaseTestCase):
    """class for user sign in test case"""

    def test_user_login(self):

        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = { "username": "alwa", "password": "LUG4Z1V4"}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 202)

    def test_user_login_with_empty_details(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "", "password": ""}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 400)
        self.assertIn("input valid username", str(res2.json))

    def test_user_login_with_empty_username(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "", "password": "12345TAHAH"}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 400)
        self.assertIn("input valid username", str(res2.json))

    def test_login_with_empty_empty_password(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "alwa", "password": ""}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 400)
        self.assertIn("input password it is empty", str(res2.json))

    def test_login_with_wrong_password(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "alwa", "password": "123444"}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 401)
        self.assertIn("wrong credentials provided", str(res2.json))

    def test_login_with_wrong_username(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "alqwey", "password": "LuG$Z!V$"}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 404)
        self.assertIn("User alqwey doesn't exist", str(res2.json))

    def test_login_with_spaces_on_details(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "  ", "password": "  "}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 400)
        self.assertIn("input valid username", str(res2.json))


if __name__ == '__main__':
    unittest.main()
