from flask import Flask, request, abort, jsonify

from models import Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/')
    def index():
        return jsonify({"message":"hello"})

    @app.route('/actors', methods=['GET'])
    def crud_actors():
        actors_formatted = []
        try:
            actors = Actor.query.all()
            for a in actors:
                actors_formatted.append(a.format)
        except ConnectionError:
            abort(503)

        return jsonify(actors_formatted)

    @app.route('/movies', methods=['GET'])
    def crud_movies():
        movies_formatted = []
        try:
            movies = Actor.query.all()
            for m in movies:
                movies_formatted.append(m.format)
        except ConnectionError:
            abort(503)

        return jsonify(movies_formatted)

    return app