from flask import Flask
from .db import db, migrate
from .models import customer, rental, video
# Import Blueprints here
from .routes.customer_routes import bp as customer_bp
from .routes.video_routes import bp as video_bp
from .routes.rental_routes import bp as rental_bp

import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(customer_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(rental_bp)
    
    return app