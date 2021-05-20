from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv # allows to bring .env variables
import os # allows us to get the .env variables with method os.environ.get

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()   # calls variables (that are text) from .env and converts
                # them into real variables so git doesn't track the,

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # when I modify my model tracks those
    # to keep order of sorted dictionary passed to jsonify() function
    app.config['JSON_SORT_KEYS'] = False 

    if test_config is None: 
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    ## this grabs my models, where my routes are and my blueprints   
    ## (grabbing it all from everywhere) to be able to run my app
    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.video import Video
    from .routes import video_bp  # Importing all routes from each model
    from .routes import customer_bp  # with the corresponding blue print
    from .routes import rental_bp ## need to create this blueprint if needed
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here   
    app.register_blueprint(customer_bp)  # registering blueprints for each model (customer)
    app.register_blueprint(video_bp)  # model (video)
    app.register_blueprint(rental_bp)  # model (rental)


    # IF ALL GOES WELL, HERE YOU APP IS READY TO work and do posts! 
    # gets, deletes, etc!
    return app
