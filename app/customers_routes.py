from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

