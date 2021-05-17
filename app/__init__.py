from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


def create_app(test_config=None):
    app = Flask(__name__)

    return app
