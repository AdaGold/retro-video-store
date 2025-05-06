from dotenv import load_dotenv
from app import create_app
from app.seed import customer
from app.seed import video

load_dotenv()

with create_app().app_context():
    customer.load()
    video.load()