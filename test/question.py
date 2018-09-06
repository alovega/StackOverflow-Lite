import unittest
from app import create_app


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client


    def test_post_question(self):
        request = {"title":"question 1","description":"sample description"}
        res = self.client().post("/questions",json=request)
        self.assertEqual(res.status_code,201)

    def test_post_question_with_empty_title(self):
        request = {"title":"", "description": "this is a sample description"}
        res = self.client().post ("/questions", json=request)
        self.assertEqual (res.status_code, 200)
        self.assertIn("title can not be empty", str(res.json))


    def test_post_question_with_empty_description(self):
        request = {"title": "question 1", "description": ""}
        res = self.client().post ("/questions", json=request)
        self.assertEqual(res.json, {"message": "description can not be empty"})

    def test_post_question_with_empty_details(self):
        request = {"title": "", "description": ""}
        res = self.client().post("/questions", json=request)
        self.assertEqual(res.status_code, 200)

    def test_get_all_question(self):
        res = self.client().get("/questions")
        self.assertEqual(res.status_code, 200)


    def test_get_non_existing_question(self):
        res = self.client().get("/question/155")
        self.assertEqual(res.status_code, 404)


    def test_get_question(self):
        request = {"title": "question1", "description": "this is a sample description"}
        res1 = self.client().post("/questions", json=request)
        print (res1.json['question']['id'])
        res2 = self.client().get("/question/3")
        print (res2.json['question'])
        self.assertEqual(res1.json['question'], res2.json['question'])



if __name__ == '__main__':
    unittest.main()