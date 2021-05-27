from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)
    # Import models here for Alembic setup.  why exactly are they necessary?
    from app.models.customer import Customer
    from app.models.video import Video
    from app.models.rental import Rental
    from .routes import customers_bp, videos_bp, rentals_bp

    app.register_blueprint(customers_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(rentals_bp)

    return app


