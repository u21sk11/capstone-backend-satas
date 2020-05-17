from flask import Flask, request, abort, jsonify

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({"message":"hello"})

    return app