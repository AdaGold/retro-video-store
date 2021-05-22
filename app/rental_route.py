from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response,jsonify
from datetime import datetime 
import requests
import json



rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rental_bp.route("", methods=["GET", "POST"])
def handle_rental_get_post_all():
    
    if request.method == "GET":
        
        
        video_list = Customer.query.all()

            
        video_response = []

        for video in video_list:
        
            video_response.append(video.json_object())
        
        return jsonify(video_response), 200

    elif request.method == "POST":

        request_body = request.get_json()

        if ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body):
            return make_response({
                "details": "Invalid data"
            }), 400
    
        new_customer = Customer(name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])

        if new_customer.registered_at == None:
            new_customer.registered_at = datetime.now()

        db.session.add(new_customer)
        db.session.commit()

        return make_response({"id": new_customer.customer_id}), 201
