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
    
    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.video import Video

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints here
    from app.routes_customers import customers_bp
    from app.routes_videos import videos_bp
    app.register_blueprint(customers_bp)
    app.register_blueprint(videos_bp)

    return app
