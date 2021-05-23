from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import request, Blueprint, jsonify
from datetime import timedelta, date

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def is_valid_data(request_body):
    if len(request_body) != 3:
        return False
    return True

def bad_request():
        return jsonify({400: "Bad Request"}), 400

def not_found():
        return jsonify({404: "Not Found"}), 404

def error_response(code=400):
    return {"details": "Invalid data"}, code
    
####################### CUSTOMER ROUTES #######################

@customers_bp.route("", methods=["GET"])
def get_customers():
    """Lists all existing customers and details about each customer."""  
    customers = Customer.query.all()
    response_body = [] 
    for customer in customers:
        response_body.append(customer.to_dict())
    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["GET"]) 
def get_customer_info(customer_id):
    """Gives back details about specific customer."""
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response(code=404)
    return customer.to_dict(), 200

@customers_bp.route("", methods = ["POST"])
def add_customer():
    """Adds new customer."""
    request_body = request.get_json()
    if not is_valid_data(request_body):
        return error_response()
    customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
        )  
    db.session.add(customer)
    db.session.commit()
    return jsonify({"id": customer.customer_id}), 201

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Updates and returns details about specific customer."""
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response(code=404)
    request_body = request.get_json()
    if not is_valid_data(request_body):
        return error_response()
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    db.session.commit()
    return customer.to_dict(), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Deletes a specific customer."""
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response(code=404)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"id": int(customer_id)}), 200

####################### VIDEO ROUTES #######################

@videos_bp.route("", methods=["GET"])
def get_videos():
    """Lists all existing videos and details about each video."""  
    videos = Video.query.all()
    response_body = [] 
    for video in videos:
        response_body.append(video.to_dict())
    return jsonify(response_body), 200

@videos_bp.route("/<video_id>", methods=["GET"]) 
def get_video_info(video_id):
    """Gives back details about specific video in the store's inventory."""
    video = Video.query.get(video_id)
    if not video:
        return error_response(code=404)
    return video.to_dict(), 200

@videos_bp.route("", methods = ["POST"])
def add_video():
    """Creates a new video with the given params."""
    request_body = request.get_json()
    if not is_valid_data(request_body):
        return error_response()
    video = Video(
        title = request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"],
        )  
    video.available_inventory = video.total_inventory
    db.session.add(video)
    db.session.commit()
    return jsonify({"id": video.video_id}), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    """Gives back details about specific video in the store's inventory."""
    video = Video.query.get(video_id)
    if not video:
        return error_response(code=404)
    request_body = request.get_json()
    if not is_valid_data(request_body):
        return error_response()
    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return video.to_dict(), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    """Deletes a specific video."""
    video = Video.query.get(video_id)
    if not video:
        return error_response(code=404)
    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": int(video_id)}), 200

####################### RENTAL ROUTES #######################

@rentals_bp.route("/check-out", methods = ["POST"])
def check_out_video():
    """Checks out a video to a customer, and updates the data in the database as such."""
    request_body = request.get_json()
    video_id = request_body.get("video_id")
    customer_id = request_body.get("customer_id")

    if type(customer_id) != int or type(video_id) != int:
        return bad_request()

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    if not customer or not video:
        return not_found()
    if video.available_inventory <= 0:
        return bad_request()

    rental = Rental(
        customer_id=customer_id, 
        video_id=video_id,
        due_date = date.today() + timedelta(days=7)
        )
    
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    
    db.session.add(rental)
    db.session.commit()

    return jsonify({
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    })

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    """Checks in a video to a customer, and updates the data in the database as such."""
    request_body = request.get_json()
    video_id = request_body.get("video_id")
    customer_id = request_body.get("customer_id")

    if type(customer_id) != int or type(video_id) != int:
        return bad_request()

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    if not customer or not video:
        return not_found()

    rental = Rental.query.filter_by(
        customer_id=customer.customer_id,
        video_id=video.video_id).one_or_none()

    if rental is None:
        return bad_request()   

    video.available_inventory += 1
    customer.videos_checked_out_count -= 1

    db.session.delete(rental)
    db.session.commit()

    return jsonify({
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }), 200

@customers_bp.route("<video_id>/rentals", methods=["GET"])
def get_customer_rentals(video_id):
    """List the videos a customer currently has checked out"""
    customer = Customer.query.get(video_id)

    if customer is None:
        return not_found()
    
    rentals = Rental.query.filter_by(customer_id=customer.customer_id)

    rental_response = []
    for rental in rentals:
        video = Video.query.get(rental.video_id)
        
        rental_response.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date
            })

    return jsonify(rental_response), 200

@videos_bp.route("<customer_id>/rentals", methods=["GET"])
def get_video_rentals(customer_id):
    """List the customers who currently have the video checked out"""
    video = Video.query.get(customer_id)

    if video is None:
        return not_found()

    rentals = Rental.query.filter_by(video_id=video.video_id)

    rental_response = []
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)

        rental_response.append({
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
            })

    return jsonify(rental_response), 200
