from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response
from flask import jsonify
from sqlalchemy import asc, desc
import datetime
import requests
import os 
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


# GET NEW CUSTOMERS*********************************************************************
@customers_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def get_customers():

    if request.method == "GET":
        customers = Customer.query.all() 

        customers_response = []

        for customer in customers:
            customers_response.append(customer.display_json())

        return jsonify(customers_response)

# POST / CREATE NEW CUSTOMERS****************************************************************
    elif request.method == "POST":
        request_body = request.get_json()
        if ("name"  or "postal_code" or "phone" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)
        
        else:
            customer = Customer(name = request_body["name"],
                            postal_code = request_body["postal_code"],
                            phone = request_body["phone"])
        if customer.registered_at == None:
            customer.registered_at = datetime.datetime.now()
        

        db.session.add(customer)
        db.session.commit()


        return make_response({
            "id": customer.customer_id}, 201)

# GET A SPECIFIC CUSTOMER ***********************************************************************
@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_customer(customer_id):

    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify({"customer": customer.display_json()}), 200


# PUT / UPDATE A SPECIFIC CUSTOMER **************************************************************
    elif request.method == "PUT":
        request_body = request.get_json()
        if ("name"  or "postal_code" or "phone" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)

        form_data = request.get_json()
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]
        db.session.commit()
        return jsonify({"customer": customer.display_json()}), 200

# DELETE A SPECIFIC CUSTOMER **********************************************************************
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id":(f'{customer.customer_id} sussesfully deleted')}), 200
    
    return {
        "message": f"Customer with id {customer.id} was not found",
        "success": False,
    }, 404



# GET VIDEOS************************************************************************************
@videos_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def get_videos():

    if request.method == "GET":
        videos = Video.query.all() 
    
        videos_response = []

        for video in videos:
            videos_response.append(video.display_json())

        return jsonify(videos_response)

# CREATE NEW VIDEOS*****************************************************************************
    elif request.method == "POST":
        request_body = request.get_json()
        if ("title"  or "release_date" or "total_inventory" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)
        else:
            video = Video(title = request_body["title"],
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"]),201
        # if video.release_date == None:
        #     video.release_date = datetime.datetime.now()
        
        db.session.add(video)
        db.session.commit()
        return make_response({"id": video.video_id}, 201)
