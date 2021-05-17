from app.models.customer import Customer
from app.models.video import Video

from app import db
from flask import request, Blueprint, make_response, jsonify

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

'''
To Do:
GET /customers
GET /customers/<id>
POST /customers
PUT /customers/<id>
DELETE /customers/<id>
'''
@customers_bp.route("", methods=["GET"])
def get_customers():
    pass