import unittest
import os
import json
from test.test_base import BaseTestCase


class TestUserSignIn(BaseTestCase):
    """class for user sign in test case"""

    def test_user_login(self):

        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request_login = { "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 200)

    def test_user_login_with_empty_details(self):
        request_login = {"username": "", "password": ""}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 200)


    def test_user_login_with_empty_username(self):
        request_login = {"username": "", "password": "12345TAHAH"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 200)

    def test_login_with_empty_empty_password(self):
        request_login = {"username": "alwa", "password": ""}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 200)

    def test_login_with_wrong_password(self):
        request_login = {"username": "alwa", "password": "123444"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 200)


    def test_login_with_wrong_username(self):
        request_login = {"username": "alqwey", "password": "LuG$Z!V$"}
        res = self.client.post("/auth/login", json=request_login)
        self.assertEqual(res.status_code, 200)


if __name__=='__main__':
    unittest.main()