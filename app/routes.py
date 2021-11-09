from app import db
from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models.video import Video

video_bp = Blueprint("videos", __name__, url_prefix=("/videos"))
#within the empty quotes for the route do I need to put "/<video>"
@video_bp.route("", methods=["POST"])
def post_video():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
                    return{
                        "details": "invalid data"
                    }, 400

db.session.add()
db.session.commit()

@video_bp.route("", methods=["GET"])
def get_video():
#list = []
 for video in list:
            ({
            "id": video.video_id,
            "title": video.title,
            "release_date": datetime.now(),
            "total_inventory": video.total_inventory
            })

@video_bp.route("/video/<id>",methods=["GET"])
# Gives back details about specific video 
# in the store's inventory.
#response 
            ({
            "id": video.video_id,
            "title": video.title,
            "release_date": datetime.now(),
            "total_inventory": video.total_inventory
            })

@video_bp.route("/video<id>",methods=["PUT"])
#this will update/replace the video id 
#should it return the same as 35-40 as above

from app.models import customer
from app.models.customer import Customer
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def post_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    elif "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    elif "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400

    new_customer = Customer(
        name = request_body["name"],
        #registered_at = request_body["registered_at"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.id}), 201

#Get
@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = []

    for customer in customers:
        customers_response.append(
            {
            "id" : customer.id,
            "name" : customer.name,
            "postal_code" : customer.postal_code,
            "phone" : customer.phone,
            "registered_at" : datetime.now()
            }
        )
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    if customer_id.isnumeric() != True:
        return {"message": "Customer id provided is not a number."}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    return {
        "id" : customer.id,
        "name" : customer.name,
        "postal_code" : customer.postal_code,
        "phone" : customer.phone
    }
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    request_body = request.get_json()
    
    if customer is None:
        return {"message": f"Customer {customer.id} was not found"}, 404

    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return {
        "details": "Invalid data"
        }, 400
        
    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]
    
    db.session.commit()

    return {
        "id" : customer.id,
        "name" : customer.name,
        "postal_code" : customer.postal_code,
        "phone" : customer.phone,
        "registered_at" : datetime.now()
    }

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id}), 200
