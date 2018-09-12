import unittest
from test.test_base import BaseTestCase


class TestUserSignUp(BaseTestCase):
    """class for user sign up test case"""

    def test_user_sign_up(self):

        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password":"LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)

    def test_user_name_empty(self):
        request = {"email": "alovegakevin@gmail.com", "username": "", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("input valid username", str(res.json))


    def test_user_email_empty(self):
        request = {"email": "", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("email not valid", str(res.json))

    def test_user_email_with_spaces(self):
        request = {"email": "    ", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("email not valid", str(res.json))

    def test_empty_password(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": ""}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("input password it is empty", str(res.json))

    def test_password_with_spaces(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "  "}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("input password it is empty", str(res.json))

    def test_sign_up_with_empty_details(self):
        request = {"email": "", "username": "", "password": ""}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("email not valid", str(res.json))



    def test_sign_up_with_already_registred_email(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request2 = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        request = self.client.post("/auth/signup", json=request2)
        self.assertEqual(request.status_code, 409)
        self.assertIn("Email already used", str(request.json))



    def test_sign_up_with_already_registered_username(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 201)
        request2 = {"email": "alwakevin@gmail.com", "username": "alwa", "password": "LUG4Z1V4"}
        request = self.client.post("/auth/signup", json=request2)
        self.assertEqual(request.status_code, 409)
        self.assertIn("username already used pick another one", str(request.json))


if __name__=='__main__':
    unittest.main()