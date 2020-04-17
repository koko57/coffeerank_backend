
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db
from flask import Flask
from controllers.coffee import coffee

def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(coffee)
    CORS(app)
    setup_db(app)
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)