from flask.globals import session
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rentals import Rental
from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ===== Customers ===================================================
customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_customers():
    query_params = request.args.get()
    if query_params.get("sort"):
        customers = Customer.query.order_by(query_params.get("sort"))\
            .paginate(page=query_params["p"], per_page=query_params["n"])
    else:
        customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers], 200)

@customers_bp.route("", methods=["POST"])
def post_customers():
    request_body = request.get_json()
    try:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            register_at=datetime.now()
        )
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)

@customers_bp.route("/<active_id>", methods=["GET"])
def get_customer(active_id):
    customer = Customer.query.get_or_404(active_id)
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<active_id>", methods=["PUT"])
def put_customer(active_id):
    customer = Customer.query.get_or_404(active_id)
    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.commit()
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<active_id>", methods=["DELETE"])
def delete_customer(active_id):
    customer = Customer.query.get_or_404(active_id)
    db.session.delete(customer)
    db.session.commit()
    return ({"id" : int(active_id)}, 200)

@customers_bp.route("/<active_id>/rentals", methods=["GET"])
def get_rentals_by_customer(active_id):
    customer = Customer.query.get_or_404(active_id)

    rental_list = []
    for rental in customer.active_rentals:
        video = Video.query.get_or_404(rental.video_id)
        rental_list.append({"release_date" : video.release_date,
            "title" : video.title,
            "due_date" : rental.due_date
            })

    return jsonify(rental_list)

# ===== Videos ======================================================
videos_bp = Blueprint("video", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@videos_bp.route("", methods=["POST"])
def post_videos():
    request_body = request.get_json()
    try:
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
        )
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_dict(), 201)

@videos_bp.route("/<active_id>", methods=["GET"])
def get_video(active_id):
    video = Video.query.get_or_404(active_id)
    return make_response(video.to_dict(), 200)

@videos_bp.route("/<active_id>", methods=["PUT"])
def put_video(active_id):
    video = Video.query.get_or_404(active_id)
    request_body = request.get_json()

    try:
        video.title=request_body["title"],
        video.release_date=request_body["release_date"],
        video.total_inventory=request_body["total_inventory"]
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.commit()
    return make_response(video.to_dict(), 200)

@videos_bp.route("/<active_id>", methods=["DELETE"])
def delete_video(active_id):
    video = Video.query.get_or_404(active_id)
    db.session.delete(video)
    db.session.commit()
    return ({"id" : int(active_id)}, 200)

@videos_bp.route("/<active_id>/rentals", methods=["GET"])
def get_rentals_by_video(active_id):
    video = Video.query.get_or_404(active_id)

    rental_list = []
    for rental in video.active_rentals:
        customer = Customer.query.get_or_404(rental.customer_id)
        rental_list.append({"name" : customer.name,
            "phone" : customer.phone,
            "postal_code" : customer.postal_code,
            "due_date" : rental.due_date
            })

    return jsonify(rental_list)

# ===== Rentals =====================================================
rentals_bp = Blueprint("rental", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_rental():
    request_body = request.get_json()

    try:
        if type(request_body["customer_id"]) is not int or type(request_body["video_id"]) is not int:
            return make_response({"details" : "Invalid data"}, 400)
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    customer = Customer.query.get_or_404(request_body["customer_id"])
    video = Video.query.get_or_404(request_body["video_id"])

    if (video.total_inventory - len(video.active_rentals)) < 1:
        return make_response({"details" : "Not available"}, 400)

    new_rental = Rental(
            customer_id=customer.id,
            video_id=video.id,
            due_date=(datetime.now() + timedelta(days=7))
        )

    db.session.add(new_rental)
    db.session.commit()

    ret_body = new_rental.to_dict()
    ret_body["videos_checked_out_count"] = len(customer.active_rentals)
    ret_body["available_inventory"] = video.total_inventory - len(video.active_rentals)

    return make_response(ret_body, 200)

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_rental():
    request_body = request.get_json()

    try:
        rental = Rental.query.filter_by(
            customer_id=request_body["customer_id"], 
            video_id=request_body["video_id"]
            ).first()
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    if not rental:
        return make_response({"details" : "Invalid data"}, 400)

    # In prod version, I would move these records to a historical database
    # For this, I am treating my Rentals as active rentals only
    db.session.delete(rental)
    db.session.commit()

    customer = Customer.query.get(rental.customer_id)
    video = Video.query.get(rental.video_id)

    ret_body = {"customer_id" : rental.customer_id,
        "video_id" : rental.video_id,
        "videos_checked_out_count" : len(customer.active_rentals),
        "available_inventory" : video.total_inventory - len(video.active_rentals)
        }

    return make_response(ret_body, 200)
