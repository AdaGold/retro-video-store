from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os



db = SQLAlchemy()
migrate = Migrate()

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
    
    app.config['JSON_SORT_KEYS'] = False



    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.video import Video
    

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import customers_bp
    from .routes import videos_bp


    

    # Register Blueprints here
    app.register_blueprint(customers_bp)
    app.register_blueprint(videos_bp)

    return app
