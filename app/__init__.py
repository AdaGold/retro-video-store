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

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
# Need lines22-25???
    # else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.video import Video
    from app.models.rental import Rental

# Register Blueprints here
    from app.customer_routes import customer_bp
    from app.video_routes import video_bp
    from app.rental_routes import rental_bp
    from app.rental_routes import customer_rental_bp
    from app.rental_routes import video_rental_bp
    
    app.register_blueprint(customer_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(rental_bp)
    app.register_blueprint(customer_rental_bp)
    app.register_blueprint(video_rental_bp)

    return app
