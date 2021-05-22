from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_json())
        
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer_by_id(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    return customer.to_json(), 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def new_customer():
    request_body = request.get_json()
    
    try:
        customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(customer)
    db.session.commit()

    return make_response({
        "id": customer.customer_id
    }, 201)

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_video(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form_data = request.get_json()

    try:
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.commit()

    return customer.to_json(), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    db.session.delete(customer)
    db.session.commit()

    return make_response({
        "id": customer.customer_id
    }, 200)

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos_index():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_json())
        
    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_video_by_id(video_id):
    video = Video.query.get_or_404(video_id)

    return video.to_json(), 200

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def new_video():
    request_body = request.get_json()
    
    try:
        video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"],
                        available_inventory=request_body["total_inventory"])

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(video)
    db.session.commit()

    return make_response({
        "id": video.video_id
    }, 201)

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    form_data = request.get_json()

    try:
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.commit()

    return video.to_json(), 200

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    
    db.session.delete(video)
    db.session.commit()

    return make_response({
        "id": video.video_id
    }, 200)

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out():
    request_body = request.get_json()

    rental = Rental(customer_id=request_body["customer_id"],
                        video_id=request_body["video_id"],
                        due_date=datetime.datetime.now() + datetime.timedelta(days=7))

    try:
        customer = Customer.query.get(int(rental.customer_id))
        video = Video.query.get(int(rental.video_id))

        if customer == None:
            return make_response({
                "details": f"Customer {customer.customer_id} not found"
            }, 404)
    
        elif video == None:
            return make_response({
                "details": f"Video {video.video_id} not found"
            }, 404)
    
    except ValueError:
        return make_response({
            "details": "Invalid id"
        }, 400) 

    if video.available_inventory < 1:
        return make_response({
            "details": f"{video.title}: No available inventory"
        }, 400)  
        
    else:
        video.available_inventory -= 1
        customer.videos_checked_out_count += 1

        db.session.add(rental)
        db.session.commit()

        return make_response({
            "customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "due_date": rental.due_date,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
            }, 200)
    
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in():
    request_body = request.get_json()

    rental = Rental(customer_id=request_body["customer_id"],
                        video_id=request_body["video_id"])
                        
    try:
        customer = Customer.query.get(int(rental.customer_id))
        video = Video.query.get(int(rental.video_id))

        if customer == None:
            return make_response({
                "details": f"Customer {customer.customer_id} not found"
            }, 404)
    
        elif video == None:
            return make_response({
                "details": f"Video {video.video_id} not found"
            }, 404)
    
    except ValueError:
        return make_response({
            "details": "Invalid id"
        }, 400) 

    if customer.videos_checked_out_count < 1:
        return make_response({
            "details": f"Customer {customer.customer_id} has no checked-out videos"
        }, 400)

    else:
        video.available_inventory += 1
        customer.videos_checked_out_count -= 1

        db.session.add(rental)
        db.session.commit()

        return make_response({
            "customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
            }, 200)
    

@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_current_rentals_by_customer_id(customer_id):
    rentals = Rental.query.filter_by(customer_id=customer_id).all()
    
    rentals_response = []

    for rental in rentals:
        rentals_response.append({
        "release_date": rental.videos.release_date,
        "title": rental.videos.title,
        "due_date": rental.due_date,
        })
    
    return jsonify(rentals_response), 200

@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customers_by_video_id(video_id):
    rentals = Rental.query.filter_by(video_id=video_id).all()
    
    rentals_response = []

    for rental in rentals:
        rentals_response.append({
        "due_date": rental.due_date,
        "name": rental.customers.name,
        "phone": rental.customers.phone,
        "postal_code": rental.customers.postal_code,
    })
        
    return jsonify(rentals_response), 200

#https://docs.sqlalchemy.org/en/14/orm/backref.html