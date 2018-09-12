import unittest
from test.test_base import BaseTestCase


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
        request_login = {"username": "", "password": ""}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 400)


    def test_user_login_with_empty_username(self):
        request_login = {"username": "", "password": "12345TAHAH"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 400)

    def test_login_with_empty_empty_password(self):
        request_login = {"username": "alwa", "password": ""}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 400)

    def test_login_with_wrong_password(self):
        request_login = {"username": "alwa", "password": "123444"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 401)


    def test_login_with_wrong_username(self):
        request_login = {"username": "alqwey", "password": "LuG$Z!V$"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 401)


    def test_login_with_spaces_on_details(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "  ", "password": "  "}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 202)


    def test_issued_authorizations_token_on_login(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = {"username": "alwa", "password": "LUG4Z1V4"}
        res2 = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res2.status_code, 202)




if __name__=='__main__':
    unittest.main()