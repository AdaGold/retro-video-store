from flask import Blueprint, request, jsonify, make_response
from app.models import customer 
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime 


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

#Post customers detail tests
@customers_bp.route("", methods=["POST"])
def create_customers():
    request_body = request.get_json()
    if not "name" in request_body or not "postal_code" in request_body or not "phone" in request_body or not "completed_at" in request_body:
        return jsonify( 
            {"errors": ["Not Found"]}), 404
    else: 
        customer = Customer(name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
            completed_at = request_body["completed_at"])

    db.session.add(customer)
    db.session.commit()

    return {
            "Id": customer.id()
        }, 201



