from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime, timedelta

from app import db
from flask import request, Blueprint, make_response, jsonify

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

'''
CRUD routes for Customers
'''
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_list = []
    for customer in customers:
        customers_list.append(customer.get_response())
    sorted_customers_list = sorted(customers_list, key = lambda i: i['id'])
    return jsonify(sorted_customers_list), 200

@customers_bp.route("/<id>", methods=["GET"])
def get_customer_id(id):
    customer = Customer.query.get(id)

    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404
    return jsonify(customer.get_response()),200

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if not valid_customer_data(request_body):
            return {"details":"Invalid data"}, 400

    new_customer = Customer(
                        name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return {"id":new_customer.id},201

@customers_bp.route("/<id>", methods=["PUT"])
def update_customer_info(id):
    customer = Customer.query.get(id)

    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404

    request_body = request.get_json()
    if not valid_customer_data(request_body):
            return {"details":"Invalid data"}, 400

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    db.session.commit()
    return jsonify(customer.get_response()), 200
    
@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404
    db.session.delete(customer)
    db.session.commit()
    return {
        "id":customer.id
    }, 200

# Helper Function to ensure request body contians valid data
def valid_customer_data(request_body):
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return False
    # elif not isinstance((request_body["name"]),str) or not isinstance((request_body["phone"]),str) or not isinstance((request_body["postal_code"]),str):
    elif (type(request_body["name"])) is not str or (type(request_body["phone"])) is not str or (type(request_body["postal_code"])) is not int:
        return False
    if "videos_checked_out_count" in request_body and (type(request_body["videos_checked_out_count"])) is not int:
        return False
    return True

'''
CRUD routes for Videos
'''
@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_list = []
    for video in videos:
        videos_list.append(video.get_response())

    return jsonify(videos_list), 200

@videos_bp.route("/<id>", methods=["GET"])
def get_video_by_id(id):
    video = Video.query.get(id)

    if video == None: 
        return {"error":f"Video ID {id} not found."}, 404
    return jsonify(video.get_response()),200

@videos_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()
    if not valid_video_data(request_body):
            return {"details":"Invalid data"}, 400
    new_video = Video(
                        title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()
    return {"id":new_video.id},201

@videos_bp.route("/<id>", methods=["PUT"])
def update_video_info(id):
    video = Video.query.get(id)

    if video == None: 
        return {"error":f"Video ID {id} not found."}, 404

    request_body = request.get_json()
    if not valid_video_data(request_body):
            return {"details":"Invalid data"}, 400

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return jsonify(video.get_response()), 200

@videos_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    video = Video.query.get(id)
    if video == None: 
        return {"error":f"Video ID {id} not found."}, 404
    db.session.delete(video)
    db.session.commit()
    return {
        "id":video.id
    }, 200

def valid_video_data(request_body):
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return False
    return True

'''
CRUD for Rental Model
'''
@rentals_bp.route("/check-out", methods=["POST"])
def check_out_rental():
    
    request_body = request.get_json()

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if customer_id == None or not isinstance(customer_id,int):
        return {"error":"Please provide a customer ID"}, 400

    if video_id == None or not isinstance(video_id,int):
        return {"error":"Please provide a video ID"}, 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer == None or video == None:
        return {"error":"Not found!"}, 404
        
    if video.total_inventory < 1 or (video.total_inventory - len(video.active_rentals)) < 1:
        return {"error":"No available inventory"},400

    due_date = ((datetime.today()) + (timedelta(days=7)))
    new_rental = Rental(customer_id=customer_id, video_id=video_id, due_date=due_date)
    db.session.add(new_rental)
    db.session.commit()
    return new_rental.get_rental_response(), 200


@rentals_bp.route("/check-in", methods=["POST"])
def check_in_rental():
    request_body = request.get_json()

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if customer_id == None or not isinstance(customer_id,int):
        return {"error":"Please provide a customer ID"}, 400

    if video_id == None or not isinstance(video_id,int):
        return {"error":"Please provide a video ID"}, 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    rental = Rental.query.filter_by(customer_id=customer_id,video_id=video_id).first()

    if rental == None:
        return {"error":"Rental not found"}, 400

    db.session.delete(rental)
    db.session.commit()

    return {
            "customer_id": customer_id,
            "video_id": video_id,
            "videos_checked_out_count": len(customer.rentals),
            "available_inventory": (video.total_inventory - len(video.active_rentals))}

@customers_bp.route("/<int:id>/rentals", methods=["GET"])
def get_customer_check_outs(id):
    customer = Customer.query.get(id)
    
    rental_list = []
    for rental in customer.rentals:
        rented_video = Video.query.get(rental.video_id)

        rental_list.append({
            "title":rented_video.title,
            "release_date":rented_video.release_date,
            "due_date":rental.due_date
        })
    return jsonify(rental_list), 200


@videos_bp.route("/<int:id>/rentals", methods=["GET"])
def get_customers_who_checked_out_video(id):
    video = Video.query.get(id)
    
    customer_list = []
    for rental in video.active_rentals:
        renting_customer = Customer.query.get(rental.customer_id)

        customer_list.append({
            "name":renting_customer.name,
            "phone":renting_customer.phone,
            "postal_code":renting_customer.postal_code,
            "due_date":rental.due_date
        })
    return jsonify(customer_list), 200
