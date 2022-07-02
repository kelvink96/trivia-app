import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

db = SQLAlchemy()

QUESTIONS_PER_PAGE = 10


# Pagination handler
def paginate_questions(req, selection):
    page = req.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]

    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'total_categories': len(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if not len(current_questions):
            abort(404)
        try:
            # get categories and refine categories
            categories = Category.query.order_by(Category.type).all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': {},
                'categories': categories_dict
            })
        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({'success': True,
                            'deleted': question_id,
                            'questions': paginate_questions(request,
                                                            Question.query.order_by(Question.id).all()),
                            'total_questions': len(Question.query.all())})

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        # check if all fields are filled
        if not new_question or not new_answer or not new_category or not new_difficulty:
            print("=== Make sure all fields are filled ===")
            abort(422)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)
            question.insert()

            return jsonify({'success': True,
                            'created': question.id,
                            'question_created': question.format(),
                            'questions': paginate_questions(request,
                                                            Question.query.order_by(Question.id).all()),
                            'total_questions': len(Question.query.all())})
        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        try:
            if search_term:
                search_results = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()

                return jsonify({
                    'success': True,
                    'search_term': search_term,
                    'questions': paginate_questions(request, search_results),
                    'total_questions': len(search_results),
                    'current_category': None
                })
        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        try:
            body = request.get_json()

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            print(previous_questions)
            if category['id'] == 0:
                questions = Question.query.filter(
                    Question.id.not_in(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category['id']).all()

            questions = [question.format() for question in questions]

            # check if there is a question
            if len(questions) > 0:
                x = random.choice(questions)

                return jsonify({
                    'success': True,
                    'question': x,
                    'previousQuestions': previous_questions
                })
            else:
                return jsonify({
                    'success': True,
                    'message': "game over"
                }), 200

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    # resource not found error
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'success': False,
                'error': 404,
                'message': "resource not found"
            }), 404
        )

    # unprocessable
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                'success': False,
                'error': 422,
                'message': 'unprocessable'
            }), 422
        )

    # bad request
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                'success': False,
                'error': 400,
                'message': 'bad request'
            }), 400)

    # internal server error
    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({
                'success': False,
                'error': 500,
                'message': 'internal server error'
            }), 500)

    return app
