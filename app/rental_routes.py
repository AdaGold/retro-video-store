from app import db, helper
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import datetime, timedelta
import os
import requests
import json

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#WAVE 2 POST/rentals/check-out
@rental_bp.route("/check-out", methods=["POST"], strict_slashes=False)

def checkout_video_to_customers():
    
    request_body = request.get_json()
    
    if ("customer_id" not in request_body or
        "video_id" not in request_body):
        return jsonify(details = "Invalid data"), 400
    
    if (type(request_body["customer_id"]) is not int or 
        type(request_body["video_id"]) is not int):
        return jsonify(details = "Invalid data"), 400    
         
    customer = Customer.query.get(request_body["customer_id"])
    if (not customer or customer == None):
        return jsonify(details = "Customer not found"), 404
    
    video = Video.query.get(request_body["video_id"])
    if (not video or video == None):
        return jsonify(details = "Video not found"), 404
   
    if (video.total_inventory - len(video.rentals)) < 1:
        return jsonify(details = " Video Not available"), 400
        
    new_rental = Rental(customer_id=customer.customer_id,
                            video_id=video.video_id,
                            due_date= datetime.now() + timedelta(days=7))
    
    db.session.add(new_rental)
    db.session.commit()
    
    response_body = new_rental.checkout_detail()
    response_body["videos_checked_out_count"] = len(customer.rentals)
    response_body["available_inventory"] = video.total_inventory -len(video.rentals)
    
    return Response(response_body), 200


#WAVE 2 POST/rentals/check-in
@rental_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def checkin_video_to_customers():
    
    request_body = request.get_json()
    
    if ("customer_id" not in request_body or
        "video_id" not in request_body):
        return jsonify(details = "Invalid data"), 400
    
    if (type(request_body["customer_id"]) is not int or 
        type(request_body["video_id"]) is not int):
        return jsonify(details = "Invalid data"), 400    
    
    rental = Rental.query.filter_by(customer_id=request_body["customer_id"], 
             video_id=request_body["video_id"]).first()
    if not rental or rental == None:
        return jsonify(details = "Invalid data"), 400
    
    db.session.delete(rental)
    db.session.commit()
    
    customer = Customer.query.get(rental.customer_id)
    video = Video.query.get(rental.video_id)
    
    if (not customer  or customer == None) or (not video or video == None):
        return jsonify(details = ""), 404
    
    response_body = {"customer_id" : rental.customer_id,
         "video_id" : rental.video_id,
         "videos_checked_out_count" : len(customer.rentals) - 1,
         "available_inventory" : video.total_inventory - len(video.rentals)
         }
    
    return Response(response_body, 200)
    
 


#OPTIONAL ENHANCEMENTS
#GET /rentals/overdue




