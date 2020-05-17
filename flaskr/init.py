from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    cors = CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PATCH,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/')
    def index():
        return jsonify({"message":"hello"})

    @app.route('/actors', methods=['GET'])
    def crud_actors():
        actors = Actor.query.all()
        actors_formatted = []
        for a in actors:
            actors_formatted.append(a.format)
        
        return jsonify(actors_formatted)

    return app