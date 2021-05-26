from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv                  # importing the package
import os                               # reads environment variables 

db = SQLAlchemy()   # creates a SQL object to interact with the database
migrate = Migrate()   # creates a migrate objest to change the structure of the database

load_dotenv()  # loads the values from .env file so that the os module can see them 

# creates a new flask app
def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.video import Video
    from app.models.rental import Rental

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import customers_bp, videos_bp, rentals_bp
    app.register_blueprint(customers_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(rentals_bp)

    return app
