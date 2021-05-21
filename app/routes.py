from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime, timedelta, date
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = [customer.to_dict() for customer in customers]
    return jsonify(customers_response)


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return ({"error": f"No customer with ID #{customer_id}"}, 404)
    return customer.to_dict()


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    
    #CONSIDER REPLACING WITH valid_customer_input() if fixed
    if "name" not in request_body:
        return ({"error": "Missing customer name"}, 400)
    if "postal_code" not in request_body:
        return ({"error": "Missing customer postal_code"}, 400)
    if "phone" not in request_body:
        return ({"error": "Missing customer phone"}, 400)
    
    new_customer = Customer(name = request_body["name"],
                    postal_code = request_body["postal_code"],
                    phone = request_body["phone"])
    new_customer.registered_at = datetime.utcnow()
    db.session.add(new_customer)
    db.session.commit()
    return ({"id": new_customer.customer_id}, 201) 


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):

    customer = Customer.query.get(customer_id)
    if not customer:
        return ({"error": f"No customer with ID #{customer_id}"}, 404)
    
    form_data = request.get_json()

    #CONSIDER REPLACING WITH valid_customer_input() if fixed
    if "name" not in form_data:
        return ({"error": "Missing customer name"}, 400)
    if "postal_code" not in form_data:
        return ({"error": "Missing customer postal_code"}, 400)
    if "phone" not in form_data:
        return ({"error": "Missing customer phone"}, 400)

    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    db.session.commit()
    return customer.to_dict()
    

# NOT CURRENTLY IN USE b/c not returning message
# consider moving this to the Customer model...
def valid_customer_input(form_data):
    if "name" not in form_data:
        return ({"error": "Missing customer name"}, 400)
    if "postal_code" not in form_data:
        return ({"error": "Missing customer postal_code"}, 400)
    if "phone" not in form_data:
        return ({"error": "Missing customer phone"}, 400)
    return True
    
    # if "name" in form_data and "postal_code" in form_data and "phone" in form_data:
    #     return True 
    # return False


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return ({"error": f"No customer with ID #{customer_id}"}, 404)
    db.session.delete(customer)
    db.session.commit()
    return make_response({"id": customer.customer_id}, 200)


@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = [video.to_dict() for video in videos]
    return jsonify(videos_response)


@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return ({"error": f"No video with ID #{video_id}"}, 404)
    return video.to_dict()


@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    #CONSIDER REPLACING WITH valid_video_input() if fixed
    if "title" not in request_body:
        return ({"error": "Missing video title"}, 400)
    if "release_date" not in request_body:
        return ({"error": "Missing video release_date"}, 400)
    if "total_inventory" not in request_body:
        return ({"error": "Missing video total_inventory"}, 400)

    new_video = Video(title = request_body["title"],
                    release_date = request_body["release_date"],
                    total_inventory = request_body["total_inventory"])
    new_video.available_inventory = new_video.total_inventory
    db.session.add(new_video)
    db.session.commit()
    return ({"id": new_video.video_id}, 201) 


# Similar question to valid_customer_input() .... 
# condsider moving this to the Video model
def valid_video_input(form_data):
    if "title" in form_data and "release_date" in form_data and "total_inventory" in form_data:
        return True 
    return False

    # if "title" not in request_body:
    #     return ({"error": "Missing video title"}, 400)
    # if "release_date" not in request_body:
    #     return ({"error": "Missing video release_date"}, 400)
    # if "total_inventory" not in request_body:
    #     return ({"error": "Missing video total_inventory"}, 400)


@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):

    video = Video.query.get(video_id)
    if not video:
        return ({"error": f"No video with ID #{video_id}"}, 404)
    
    form_data = request.get_json()
    
    #CONSIDER REPLACING WITH valid_video_input() if fixed
    if "title" not in form_data:
        return ({"error": "Missing video title"}, 400)
    if "release_date" not in form_data:
        return ({"error": "Missing video release_date"}, 400)
    if "total_inventory" not in form_data:
        return ({"error": "Missing video total_inventory"}, 400)

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]
    db.session.commit()
    return video.to_dict()


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return ({"error": f"No video with ID #{video_id}"}, 404)
    db.session.delete(video)
    db.session.commit()
    return make_response({"id": video.video_id}, 200)


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video_to_customer():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if customer_id == None or not type(customer_id) is int:
        return ({"error": "Please provide a valid customer ID"}, 400)
    if video_id == None or not type(video_id) is int:
        return ({"error": "Please provide a valid video ID"}, 400)
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer == None:
        return ({"error": "Customer not found."}, 404)
    if video == None:
        return ({"error": "Video not found."}, 404)
    if video.available_inventory == 0:
        return ({"error": "No available inventory."}, 400)
    
    new_rental = Rental(customer_id = customer_id, 
                        video_id = video_id)
    new_rental.due_date = date.today() + timedelta(days=7)
    db.session.add(new_rental)
    customer.check_out()
    video.check_out()
    db.session.commit()
    return make_response({"customer_id": customer.customer_id,
                "video_id": video.video_id,
                "due_date": new_rental.due_date,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory}, 200)

# Similar question to the other "valid" helper functions ... 
# condsider moving this to the Rental model
# not currently being used .... 
def valid_rental_input(form_data):
    if "customer_id" in form_data and "video_id" in form_data:
        if type(form_data["customer_id"]) is int and type(form_data["video_id"]) is int:
            return True 
    return False


@rentals_bp.route("/check-in", methods=["POST"]) 
def check_in_video():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if customer_id == None or not type(customer_id) is int:
        return ({"error": "Please provide a valid customer ID"}, 400)
    if video_id == None or not type(video_id) is int:
        return ({"error": "Please provide a valid video ID"}, 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer == None:
        return ({"error": "Customer not found."}, 404)
    if video == None:
        return ({"error": "Video not found."}, 404)
    
    # check that customer has a video checked out
    # this function doesn't handle situations where a customer might 
    # try to return a video that isn't checked out to them ... 
    if customer.videos_checked_out_count == 0:
        return ({"error": "You don't have any videos checked out."}, 400)

    rental = Rental.query.filter_by(
                customer_id=customer_id,
                video_id=video_id)

    if not rental:
        return {"error": "Rental not found."}, 400

    customer.check_in()
    video.check_in()
    db.session.commit()
    return ({"customer_id": customer.customer_id,
                "video_id": video.video_id,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory}, 200)


@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found."}, 400
    rental_list = []
    for rental in customer.rentals:
        video = Video.query.get(rental.video_id)
        video_info = {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date
        }
        rental_list.append(video_info)
    return jsonify(rental_list)


@videos_bp.route("<video_id>/rentals", methods=["GET"])
def get_customers_by_rental(video_id):
    video = Video.query.get(video_id)
    if not video:
        return {"error": "Video not found."}, 400
    customer_list = []
    for rental in video.rentals:
        customer = Customer.query.get(rental.customer_id)
        customer_info = {
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            "due_date": rental.due_date
        }
        customer_list.append(customer_info)
    return jsonify(customer_list)