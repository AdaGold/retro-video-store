from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os # This built-in module provides a way to read environment variables
from dotenv import load_dotenv # The python-dotenv package specifies to import the package like this

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() # The python-dotenv package specifies to call this method, which loads the values from our .env file so that the os module is able to see them.

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # the connection string to connect the database to Flask is located in .env
    if test_config is None:
        # Check the keyword argument test_config. When we call create_app(), if test_config is falsy (None or empty), that means we are not trying to run the app in a test environment.
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else: # If there is a test_config passed in, this means we're trying to test the app, which can have special test settings
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")   
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.customer import Customer
    from app.models.video import Video
    from app.models.rental import Rental
    # ^^Make new models visible to flask migration helper
    
    from app.routes import customers_bp
    app.register_blueprint(customers_bp)

    from app.routes import videos_bp
    app.register_blueprint(videos_bp)

    from app.routes import rentals_bp
    app.register_blueprint(rentals_bp)
    # ^^ Register Blueprints here

    return app
    