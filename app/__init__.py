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

    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.video import Video

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here - Flask requires us to register it with app. We need to tell the app that it should use the endpoints from tasks_bp for its routing
    # customer routes
    from .routes import customer_bp
    app.register_blueprint(customer_bp)

    # video routes 
    from .routes import videos_bp
    app.register_blueprint(videos_bp)



    return app






