from flask import Blueprint
from app import db
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from flask import request, jsonify, make_response
from datetime import datetime, timedelta

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#helper functions
def customer_not_found(customer_id):
    return make_response({"error": f"Customer {customer_id} Not Found"}, 404)

def video_not_found(video_id):
    return make_response({"error": f"Video {video_id} Not Found"}, 404)

#Customer CRUD
@customer_bp.route("", methods = ["POST"], strict_slashes = False)
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"details": "Invalid data"}), 400
    
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"],
                            register_at= datetime.now())
    
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)

@customer_bp.route("", methods = ["GET"], strict_slashes = False)
def get_all_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append(customer.to_json())
    
    return make_response(jsonify(customer_list), 200)

@customer_bp.route("/<customer_id>", methods = ["GET"], strict_slashes = False)
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return make_response(customer.to_json(), 200)

    return customer_not_found(customer_id)

@customer_bp.route("/<customer_id>", methods = ["PUT"], strict_slashes = False)
def edit_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()
    if not customer:
        return customer_not_found(customer_id)
    if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
        return make_response({"message": "Invalid data"}, 400)

    customer.name = form_data.get("name")
    customer.postal_code = form_data.get("postal_code")
    customer.phone = form_data.get("phone")
    #customer.register_at = form_data["registered_at"]

    db.session.commit()
    return make_response(customer.to_json(), 200)

@customer_bp.route("/<customer_id>", methods = ["DELETE"], strict_slashes = False)
def delete_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return make_response({
            "id": int(customer_id)
        }, 200)
    
    return customer_not_found(customer_id)

#Videos CRUD
@video_bp.route("", methods= ["POST", "GET"])
def handle_video():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({"details": "Invalid data" }), 400
        
        new_video = Video(title=request_body["title"],release_date=request_body["release_date"],total_inventory=request_body["total_inventory"],available_inventory=request_body["total_inventory"])
        
        db.session.add(new_video)
        db.session.commit()
        return make_response({
            "id": new_video.video_id
        }, 201)
    
    elif request.method == "GET":
        videos = Video.query.all()

        video_list = []
        for video in videos:
            video_list.append(video.to_json())

        return make_response(jsonify(video_list), 200)

@video_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def deal_w_video(video_id):
    video = Video.query.get(video_id)

    if not video:
        return video_not_found(video_id)
    if request.method == "GET":
        return make_response(
            video.to_json()
        , 200)
    elif request.method == "PUT":
        form_data = request.get_json()
        if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
            return make_response({"message": "Invalid data"}, 400)
        video.title = form_data.get("title")
        video.release_date = form_data.get("release_date")
        video.total_inventory = form_data.get("total_inventory")
        db.session.commit()
        return make_response(
            video.to_json()
        , 200)
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({"id": int(video_id)}, 200)

###Wave 2 Custom Endpoints
def is_id(input):
    condition = isinstance(input, int)
    return True if condition else False

@rental_bp.route("/check-out", methods = ["POST"])
def check_out():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if not is_id(customer_id):
        return make_response({"error": "customer ID must be an integer"}, 400)
    elif not is_id(video_id):
        return make_response({"error": "customer ID must be an integer"}, 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if not customer:
        return customer_not_found(customer_id)
    if not video:
        return video_not_found(video_id)

    if video.available_inventory == 0:
        return make_response({"details": "No inventory available"}, 400)

    video.available_inventory -= 1
    customer.videos_checked_out_count += 1
    due_date = datetime.now() + timedelta(days=7)

    new_rental = Rental(customer_id = request_body["customer_id"], video_id = request_body["video_id"], due_date = due_date)
    db.session.add(new_rental)
    db.session.commit()
    
    check_out_rental = new_rental.to_json()
    check_out_rental["videos_checked_out_count"] = customer.videos_checked_out_count 
    check_out_rental["available_inventory"] = video.available_inventory

    return make_response(check_out_rental, 200)

@rental_bp.route("/check-in", methods = ["POST"])
def check_in():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if not is_id(customer_id):
        return make_response("customer ID must be an integer", 400)
    elif not is_id(video_id):
        return make_response("video ID must be an integer", 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if not customer:
        return customer_not_found(customer_id)
    if not video:
        return video_not_found(video_id)
    
    if customer.videos_checked_out_count == 0:
        return make_response({"details": "All videos are returned"}, 400)

    video.available_inventory += 1
    customer.videos_checked_out_count -= 1

    new_rental = Rental(customer_id = request_body["customer_id"], video_id = request_body["video_id"])
    db.session.add(new_rental)
    db.session.commit()
    
    return make_response({
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    },200)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def rental_video_by_id(video_id):
    rental_results = db.session.query(Customer, Video, Rental).join(
        Video, Video.video_id==Rental.video_id).join(
        Customer, Customer.customer_id==Rental.customer_id).filter(
        Video.video_id==video_id).all()
    
    if rental_results:
        video_rental_list = []
        for index in rental_results:
            customer = index[0]
            rental = index[2]
            video_rental_list.append({
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": customer.postal_code,
                "due_date": rental.due_date
            })
        return make_response(jsonify(video_rental_list), 200)
    else:
        return video_not_found(video_id)

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def rental_customer_by_id(customer_id):
    rental_results = db.session.query(Customer, Video, Rental).join(
        Video, Video.video_id==Rental.video_id).join(
        Customer, Customer.customer_id==Rental.customer_id).filter(
        Customer.customer_id==customer_id).all()

    if rental_results:
        customer_rental = []
        for index in rental_results:
            video = index[1]
            rental = index[2]
            customer_rental.append({
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental.due_date
            })

        return make_response(jsonify(customer_rental), 200)
    else:
        return customer_not_found(customer_id)