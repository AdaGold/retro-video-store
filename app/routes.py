from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, jsonify

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

def is_valid_customer_data(request_body):
    if len(request_body) != 3 or \
        "name" not in request_body or  \
        "postal_code" not in request_body or \
        "phone" not in request_body:
        return False
    return True

def is_valid_video_data(request_body):
    if len(request_body) != 3 or \
        "title" not in request_body or  \
        "release_date" not in request_body or \
        "total_inventory" not in request_body:
        return False
    return True

def get_client_error_response(code=400):
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
        return get_client_error_response(code=404)
    return customer.to_dict(), 200

@customers_bp.route("", methods = ["POST"])
def add_customer():
    """Adds new customer."""
    request_body = request.get_json()
    if not is_valid_customer_data(request_body):
        return get_client_error_response()
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
        return get_client_error_response(code=404)
    request_body = request.get_json()
    if not is_valid_customer_data(request_body):
        return get_client_error_response()
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
        return get_client_error_response(code=404)
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
        return get_client_error_response(code=404)
    return video.to_dict(), 200

@videos_bp.route("", methods = ["POST"])
def add_video():
    """Creates a new video with the given params."""
    request_body = request.get_json()
    if not is_valid_video_data(request_body):
        return get_client_error_response()
    video = Video(
        title = request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"]
        )  
    db.session.add(video)
    db.session.commit()
    return jsonify({"id": video.video_id}), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    """Gives back details about specific video in the store's inventory."""
    video = Video.query.get(video_id)
    if not video:
        return get_client_error_response(code=404)
    request_body = request.get_json()
    if not is_valid_video_data(request_body):
        return get_client_error_response()
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
        return get_client_error_response(code=404)
    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": int(video_id)}), 200