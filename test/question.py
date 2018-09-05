import unittest
from app import create_app


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client


    def test_post_question(self):
        request = {"title":"question 1","description":"sample description"}
        res = self.client().post("/questions",json=request)
        self.assertEqual(res.status_code,203)

    def test_post_question_with_empty_title(self):
        request = {"title":"", "description": "this is a sample description"}
        res = self.client().post ("/questions", json=request)
        self.assertEqual (res.status_code, 200)
        self.assertIn("please input question title", str(res.json))


    def test_post_question_with_empty_description(self):
        request = {"title": "question 1", "description": ""}
        res = self.client().post ("/questions", json=request)
        self.assertEqual(res.json, {"message": "please input question description"})

    def test_post_question_with_empty_details(self):
        request = {"title": "", "description": ""}
        res = self.client().post("/questions", json=request)
        self.assertEqual(res.status_code, 400)

    def test_get_all_question(self):
        res = self.client().get("/questions")
        self.assertEqual(res.status_code, 200)


    def test_get_non_existing_question(self):
        res = self.client().get("/question/15")
        self.assertEqual(res.status_code, 400)


    def test_get_question(self):
        request = {"title": "question1", "description": "this is a sample description"}
        res = self.client().post("/questions", json=request)
        res2 = self.client().get("/question/<int:id>")
        self.assertEqual(request, str(res2))



if __name__ == '__main__':
    unittest.main()