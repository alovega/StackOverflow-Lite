import unittest
import os
import json
from test.test_base import BaseTestCase


class TestUserSignUp(BaseTestCase):
    """class for user sign up test case"""

    def test_user_sign_up(self):

        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password":"LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 200)




if __name__=='__main__':
    unittest.main()