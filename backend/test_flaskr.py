import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432',
                                                               self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "Which is the highest mountain in the world", "answer": "Mount Everest",
                             "category": "3", "difficulty": "3"}
        self.new_question_error = {"question": "Which is the highest mountain in the world", "answer": "Mount Everest",
                                   "category": "Geography", "difficulty": "3"}
        self.new_search = {"searchTerm": "What boxer's original name is Cassius Clay?"}
        self.new_quizzes = {'previous_questions': [], 'quiz_category': {'type': 'Entertainment', 'id': 5}}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test get categories
    def test_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # test get questions
    def test_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # 404 when page length beyond limit
    def test_404_exceeded_page_length(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test delete a question
    def test_delete_question(self):
        question = Question(question='test question', answer='test answer',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id

        questions_before = Question.query.all()
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()

        questions_after = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)
        # check for decrease in questions
        self.assertTrue(len(questions_before) > len(questions_after))

    # test create a question
    def test_create_new_question(self):
        questions_before = Question.query.all()
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        questions_after = Question.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # check for increase in questions
        self.assertTrue(len(questions_before) < len(questions_after))

    # test if creation fails
    def test_422_question_creation_fails(self):
        questions_before = Question.query.all()
        res = self.client().post('/questions', json=self.new_question_error)
        data = json.loads(res.data)

        questions_after = Question.query.all()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        # check for questions count is same
        self.assertTrue(len(questions_before) == len(questions_after))

    # test search with results
    def test_search_question_with_results(self):
        res = self.client().post('/questions/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["total_questions"])
        self.assertIsNotNone(data["questions"])

    # test search without results
    def test_search_question_without_results(self):
        res = self.client().post('/questions/search', json={"searchTerm": "abcdefgh"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    # test get questions by category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # try to get questions from an unknown category
    def test_404_get_questions_by_category(self):
        response = self.client().get('/categories/a/questions')
        data = json.loads(response.data)

        # check status code, false success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # test if play quizzes is working
    def test_play_quizzes(self):
        res = self.client().post('/quizzes', json=self.new_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test if error occurs when playing quizzes
    def test_422_play_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
