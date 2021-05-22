from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()



def create_app(test_config=None):
    app = Flask(__name__)
#db configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI']= "postgresql+psycopg2://postgres:postgres@localhost:5432/video_store_api_development"

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.video import Video
    from app.models.customer import Customer
    from app.models.rental import Rental

    
    db.init_app(app)
    migrate.init_app(app, db)

    from.routes import video_bp, customer_bp, rental_bp
    app.register_blueprint(video_bp)
    app.register_blueprint(customer_bp)    
    app.register_blueprint(rental_bp)

    return app
