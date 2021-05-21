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
    
    # check if the required request parameters are present in request body
    if ("customer_id" not in request_body or
        "video_id" not in request_body):
        return jsonify(details = "Invalid data"), 400
    
    #check if the type is integer
    if not helper.is_int(request_body["customer_id"]) or not helper.is_int(request_body["video_id"]):
        return jsonify(details = "Invalid data"), 400      
         
    # use the request params to get the customer and video records from the DB
    customer = Customer.query.get(request_body["customer_id"])
    if (not customer or customer == None):
        return jsonify(details = "Customer not found"), 404
    
    video = Video.query.get(request_body["video_id"])
    if (not video or video == None):
        return jsonify(details = "Video not found"), 404
   
    if video.available_inventory == 0:
        return jsonify(details = " Video Not available"), 400
    
    # update the counts for the customer and video records in the DB
    video.available_inventory -= 1 # customer checked out video
    customer.videos_checked_out_count += 1 # customer checked out a new video
    
    #create new rental record
    new_rental = Rental(customer_id=customer.customer_id,
                            video_id=video.video_id,
                            due_date= datetime.now() + timedelta(days=7))
    
    #add the new rental record, video and customer in the db for the customer
    db.session.add(new_rental)
    db.session.add(video)
    db.session.add(customer)
    db.session.commit()
    
    response_body = new_rental.checkout_detail(customer, video)
    
    return response_body, 200


#WAVE 2 POST/rentals/check-in
@rental_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def checkin_video_to_customers():
    
    request_body = request.get_json()
    
    # check if the required request parameters are present in request body
    if ("customer_id" not in request_body or
        "video_id" not in request_body):
        return jsonify(details = "Invalid data"), 400
    
    if not helper.is_int(request_body["customer_id"]) or not helper.is_int(request_body["video_id"]):
        return jsonify(details = "Invalid data"), 400    
    
    # use the request params to get the customer and video records from the DB
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])
    
    if (not customer  or customer == None) or (not video or video == None):
        return jsonify(details = ""), 404
    
    # get the corresponding rental record for the customer who is checked in the video
    rental = Rental.query.filter_by(customer_id=request_body["customer_id"], 
            video_id=request_body["video_id"]).first()
    
    if not rental or rental == None:
        return jsonify(details = "Invalid data"), 400

    # update the counts for the customer and video records in the DB
    customer.videos_checked_out_count -= 1
    video.available_inventory += 1
    
    db.session.add(customer)
    db.session.add(video)
    # delete the rental record for customer who checked in the video
    db.session.delete(rental)
    db.session.commit()
    
    response_body = {
            "customer_id" : rental.customer_id,
            "video_id" : rental.video_id,
            "videos_checked_out_count" : customer.videos_checked_out_count,
            "available_inventory" : video.available_inventory
         }
    
    return response_body, 200
    

#OPTIONAL ENHANCEMENTS
#GET /rentals/overdue




