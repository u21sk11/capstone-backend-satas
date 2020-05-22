from flask import Flask, request, abort, jsonify
from datetime import datetime

from models import db, Movie, Actor
from auth import requires_auth, AuthError

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
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors(payload):
        actors_formatted = []
        page = request.args.get('page', 1, type=int)
        try:
            all_actors = Actor.query.order_by(Actor.id).all()
            actors = pagination(page, all_actors)
            for a in actors:
                actors_formatted.append(a.format())
        except ConnectionError:
            abort(503)

        return jsonify(actors_formatted)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def patch_actors(payload, id):
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']

        if len(gender) != 1:
            abort(400)
        try:
            actor = Actor.query.get(id)
            if actor is None:
                abort(404)
            else:
                actor.name = name
                actor.age = age
                actor.gender = gender
                actor.patch()
        except ConnectionError:
            abort(503)

        return jsonify({'success': True, 'actor': name})

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actors(payload, id):
        try:
            actor = Actor.query.get(id)
            if actor is None:
                abort(404)
            else:
                actor.delete()
        except ConnectionError:
            abort(503)

        return jsonify({'success': True, 'deleted_id': id})

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actors")
    def post_actors(payload):
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

        return jsonify({'success': True, 'actor': name})

    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies(payload):
        movies_formatted = []
        page = request.args.get('page', 1, type=int)
        try:
            all_movies = Movie.query.order_by(Movie.id).all()
            movies = pagination(page, all_movies)
            for m in movies:
                movies_formatted.append(m.format())
        except ConnectionError:
            abort(503)

        return jsonify(movies_formatted)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def patch_movies(payload, id):
        title = request.get_json()['title']
        date_string = request.get_json()['release_date']
        release_date = datetime.strptime(date_string, '%d %B, %Y')
        try:
            movie = Movie.query.get(id)
            if movie is None:
                abort(404)
            else:
                movie.title = title
                movie.release_date = release_date
                movie.patch()
        except ConnectionError:
            abort(503)

        return jsonify({'success': True, 'movie': title})

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movies(payload, id):
        try:
            movie = Movie.query.get(id)
            if movie is None:
                abort(404)
            else:
                movie.delete()
        except ConnectionError:
            abort(503)

        return jsonify({'success': True, 'deleted_id': id})

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movies")
    def post_movies(payload):
        title = request.get_json()['title']
        date_string = request.get_json()['release_date']
        release_date = datetime.strptime(date_string, '%d %B, %Y')

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
        except ConnectionError:
            abort(503)

        return jsonify({'success': True, 'movie': title})

    # Error Handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
                }), 404

    @app.errorhandler(503)
    def network_error(error):
        return jsonify({
            "success": False,
            "error": 503,
            "message": "issues communicating with the database"
            }), 503

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app
