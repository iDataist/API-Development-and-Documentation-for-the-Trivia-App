from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy import func
import logging
from models import *

QUESTIONS_PER_PAGE = 10
def paginate_questions(selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    questions = formatted_questions[start:end]
    return questions
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    logging.basicConfig(filename='app.log',level=logging.DEBUG)

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    #@cross_origin
    def get_categories():
        categories = Category.query.all()
        categories_dict = {category.id : category.type for category in categories}
        if len(categories) == 0:
            abort(404)
        try:
            return jsonify({
                'success': True,
                'categories': categories_dict,
                'total_categories':len(categories)
                })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    @app.route('/questions')
    #@cross_origin
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate_questions(questions)
        categories = Category.query.all()
        categories_dict = {category.id : category.type for category in categories}
        if (len(questions) == 0) or (len(categories) == 0):
            abort(404)
        try:
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': categories_dict
                })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.filter(Category.id==category_id).one_or_none()
        questions = Question.query.filter(Question.category==category_id).all()
        if (not category) or (len(questions) == 0):
            abort(404)
        try:
            return jsonify({
                'success': True,
                'questions': paginate_questions(questions),
                'total_questions': len(questions),
                'current_category': category.type
            })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_specific_question(question_id):
        question = Question.query.filter(Question.id==question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            questions = Question.query.order_by(Question.id).all()
            return jsonify({
                'success': True,
                'deleted': question_id, 
                'questions':paginate_questions(questions),
                'total_questions':len(questions)
                })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        search = body.get('searchTerm', None)
        try:
            if search:
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
                if len(questions) == 0:
                    abort(404)
                return jsonify({
                'success': True,
                'questions': paginate_questions(questions),
                'total_questions': len(questions)
                })
            else:
                new_question = body.get('question', None)
                new_answer = body.get('answer', None)
                new_category = body.get('category', None)
                new_difficulty = body.get('difficulty', None)
                if (new_question is None) or (new_answer is None) or (new_category is None) or (new_difficulty is None):
                    abort(404)
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty)
                question.insert()
                questions = Question.query.order_by(Question.id).all()
                return jsonify({
                    'success': True,
                    'created': question.id, 
                    'questions':paginate_questions(questions),
                    'total_questions':len(questions)
                    })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def create_quiz_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        if (previous_questions is None) or (quiz_category is None):
            abort(404)
        category_id = int(quiz_category['id'])
        try:
            if category_id == 0:
                question = Question.query.order_by(func.random()).filter(Question.id.notin_(previous_questions)).first()
            else:
                question = Question.query.order_by(func.random()).filter(Question.category==quiz_category['id'], \
                                                   Question.id.notin_(previous_questions)).first()
            return jsonify({
            'success': True,
            'question': question.format()
            })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    return app

