from flask import Flask, request, abort, jsonify

from models import set_up, Movie

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({"message":"hello"})

    return app