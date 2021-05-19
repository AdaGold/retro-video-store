from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response, jsonify
import datetime


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

def is_valid_data(request_body):
    if len(request_body) != 3:
        return False
    return True

'''
CUSTOMER ROUTES
'''
### Lists all existing customers and details about each customer ###
@customers_bp.route("", methods=["GET"])

def get_customers():

    # sort = request.args.get("sort")
    # page_size = request.args.get("n")
    # page_number = request.args.get("p")

    # sort_order_dict = { 'name': Customer.name.asc(), 'id': Customer.id.asc() }
    # sort_order = sort_order_dict[sort]

    # Customer.query.order_by(sort_order).offset(offset).limit(count).all()
    query_param_value = request.args.get("sort")
    if query_param_value == "name":
        customers = Customer.query.order_by(Customer.name.asc())
    else:
        customers = Customer.query.all()

    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

### Gives back details about specific customer ###
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)

def get_one_customer(customer_id):
    # Find the task with the given id
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)

    return customer.to_dict()

### Creates a new customer with the given params ###
@customers_bp.route("", methods=["POST"])

def create_customer():
    request_body = request.get_json()
        
    # Invalid task if missing title, description, or completed_at     
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({"details": "Invalid data"}), 400        
    else:
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"]
           )
        
        if new_customer.registered_at == None:
            new_customer.registered_at = datetime.datetime.now()
        
        # add this model to the database and commit the changes
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"id": new_customer.customer_id}), 201

### Updates and returns details about specific customer ###
@customers_bp.route("/<customer_id>", methods=["PUT"])

def update_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)

    new_data = request.get_json()

    if not is_valid_data(new_data):
        return make_response("{}", 400)

    customer.name = new_data["name"],
    customer.postal_code = new_data["postal_code"],
    customer.phone = new_data["phone"]

    db.session.commit()
    # return customer.to_dict(), 200
    return make_response(jsonify(customer.to_dict()), 200)

### Deletes a specific customer ###
@customers_bp.route("/<customer_id>", methods=["DELETE"])

def delete_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.customer_id}), 200

'''
VIDEO ROUTES
'''
### Lists all existing videos and details about each video ###

@videos_bp.route("", methods=["GET"])

def get_videos():

    query_param_value = request.args.get("sort")
    if query_param_value == "title":
        videos = Video.query.order_by(Video.title.asc())
    elif query_param_value == "release_date":
        videos = Video.query.order_by(Video.release_date.asc())
    else:
        videos = Video.query.all()

    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200

### Gives back details about specific video in the store's inventory ###

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)

def get_one_video(video_id):
    # Find the task with the given id
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)

    return video.to_dict(), 200

### Creates a new video with the given params ###

@videos_bp.route("", methods=["POST"])

def create_video():
    request_body = request.get_json()
        
    # Invalid task if missing title, description, or completed_at     
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({"details": "Invalid data"}), 400        
    else:
        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
           )
        
        if new_video.release_date == None:
            new_video.release_date = datetime.datetime.now()
        
        # add this model to the database and commit the changes
        db.session.add(new_video)
        db.session.commit()

        return jsonify({"id": new_video.video_id}), 201

### Updates and returns details about specific video ###
@videos_bp.route("/<video_id>", methods=["PUT"])

def update_video(video_id):

    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)

    new_data = request.get_json()

    if not is_valid_data(new_data):
        return make_response("", 400)

    video.title = new_data["title"],
    video.release_date = new_data["release_date"],
    video.total_inventory = new_data["total_inventory"]

    db.session.commit()
    return make_response(jsonify(video.to_dict()), 200)

### Deletes a specific video ###
@videos_bp.route("/<video_id>", methods=["DELETE"])

def delete_video(video_id):

    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)

    db.session.delete(video)
    db.session.commit()

    return jsonify({"id": video.video_id}), 200