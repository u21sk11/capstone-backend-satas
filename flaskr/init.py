from flask import Flask, request, abort, jsonify

from models import db, Movie, Actor

ITEMS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    def pagination(page, item):
        start = (page - 1) * 10
        end = start + 10
        return item[start:end]
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/')
    def index():
        return jsonify({"message":"hello"})

    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors_formatted = []
        page = request.args.get('page', 1, type=int)
        try:
            all_actors = Actor.query.order_by(Actor.id).all()
            actors = pagination(page, all_actors)
            for a in actors:
                actors_formatted.append(a.format)
        except ConnectionError:
            abort(503)

        return jsonify(actors_formatted)
    
    @app.route('/actors', methods=['POST'])
    def post_actors():
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        
        if len(gender) != 1:
            abort(400)

        try:
            actor = Actor(age=age, name=name, gender=gender)
            actor.insert()
        except ConnectionError:
            abort(503)
        
        return jsonify({'success': true, 'actor': name})


    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies_formatted = []
        page = request.args.get('page', 1, type=int)
        try:
            all_movies = Movie.query.order_by(Movie.id).all()
            movies = pagination(page, all_movies)
            for m in movies:
                movies_formatted.append(m.format)
        except ConnectionError:
            abort(503)

        return jsonify(movies_formatted)

    return app