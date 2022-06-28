from test_base import  *


class TestUserSignUp(BaseTestCase):
    """class for user sign up test case"""
    
    def test_user_sign_up(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name": "pass", "password":"LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)

    def test_user_name_empty(self):
        request = {"email": "alovegakevin@gmail.com", "username": "kelvin", "name":"", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("name", str(res.json))


    def test_user_email_empty(self):
        request = {"email": "", "username": "alwa", "name":"pass", "password": "LUG4Z1V4"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Not a valid email address", str(res.json))

    def test_empty_password(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "password": "", }
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("password", str(res.json))

    def test_empty_name_(self):
        request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name":"", "password": "pass"}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("name", str(res.json))

    def test_sign_up_with_empty_details(self):
        request = {"email": "", "username": "", "password": ""}
        res = self.client.post("/auth/signup", json=request)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Missing data for required field", str(res.json))


    def test_use_existing_email(self):
        with self.app.app_context():
            request = {"email":"alovega@gmail.com", "username":"alwa", "name":"kelvin", "password":"LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request2 = {"email":"alovega@gmail.com", "username":"alwa", "name":"kelvin", "password":"LUG4Z1V4"}
            req2 = self.client.post("/auth/signup", json=request2)
            self.assertEqual(req2.status_code, 403)
            self.assertIn("email already exists", str(req2.json))



    def test_sign_up_with_already_registered_username(self):
        with self.app.app_context():
            request = {"email": "alovegakevin@gmail.com", "username": "alwa", "name":"kelvin", "password": "LUG4Z1V4"}
            res = self.client.post("/auth/signup", json=request)
            self.assertEqual(res.status_code, 201)
            request2 = {"email": "alwakevin@gmail.com", "username": "alwa", "name":"kelvin", "password": "LUG4Z1V4"}
            request = self.client.post("/auth/signup", json=request2)
            self.assertEqual(request.status_code, 403)
            self.assertIn("username already used", str(request.json))


if __name__=='__main__':
    unittest.main()
