import requests
from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# START OF CUSTOMER CRUD ROUTES


@customers_bp.route("", methods=["GET"])
def list_all_customers():
    customers_response = [customer.as_dict() for customer in Customer.query.all()]
    return jsonify(customers_response)


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if invalid_customer_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    customer = Customer(name=request_body["name"], postal_code=request_body["postal_code"], phone=request_body["phone"])

    db.session.add(customer)
    db.session.commit()

    return make_response({"id": customer.customer_id}, 201)


def invalid_customer_post_request_body(request_body):
    if ("name" not in request_body or "postal_code" not in request_body or "phone" not in request_body):
        return True
    return False


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.as_dict())


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    request_body = request.get_json()
    if invalid_customer_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.add(customer)
    db.session.commit()

    return make_response(customer.as_dict(), 200)


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()
    return make_response(
        jsonify(
            details="customer \"{customer.name}\" successfully deleted", id=customer.customer_id),
        200)


@customers_bp.route("/<int:customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    rentals = [{"release_date": rental.video.release_date.strftime("%Y-%m-%d"), "title": rental.video.title,
                "due_date": rental.due_date.strftime("%Y-%m-%d")} for rental in customer.videos]

    return make_response(jsonify(rentals), 200)


# START OF VIDEO CRUD ROUTES


@videos_bp.route("", methods=["GET"])
def list_all_videos():
    videos_response = [video.as_dict() for video in Video.query.all()]
    return jsonify(videos_response)


@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if invalid_video_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"])

    db.session.add(video)
    db.session.commit()

    return make_response({"id": video.video_id}, 201)


def invalid_video_post_request_body(request_body):
    if ("title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body):
        return True
    return False


@videos_bp.route("/<int:video_id>", methods=["GET"])
def get_video_by_id(video_id):
    video = Video.query.get_or_404(video_id)
    return jsonify(video.as_dict())


@videos_bp.route("/<int:video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get_or_404(video_id)

    request_body = request.get_json()
    if invalid_video_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.add(video)
    db.session.commit()

    return make_response(video.as_dict(), 200)


@videos_bp.route("/<int:video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)

    db.session.delete(video)
    db.session.commit()
    return make_response(jsonify(details="video \"{video.name}\" successfully deleted", id=video.video_id), 200)


@videos_bp.route("/<int:video_id>/rentals", methods=["GET"])
def get_rentals_by_video(video_id):
    video = Video.query.get_or_404(video_id)

    rentals = [
        {"name": rental.customer.name,
         "phone": rental.customer.phone,
         "postal_code": rental.customer.postal_code,
         "due_date": rental.due_date.strftime("%Y-%m-%d")}
        for rental in video.customers]

    return make_response(jsonify(rentals), 200)


# START OF RENTALS ENDPOINTS


def invalid_check_out_request_body(request_body):
    if "customer_id" not in request_body or "video_id" not in request_body:
        return True

    if not is_integer(request_body["video_id"]) or not is_integer(request_body["customer_id"]):
        return True

    video = Video.query.get_or_404(request_body["video_id"])

    if video.get_inventory() == 0:
        return True

    if Rental.query.get((request_body["customer_id"], request_body["video_id"])):
        return True
    return False


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()

    if invalid_check_out_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"])

    db.session.add(rental)
    db.session.commit()
    rental_dict = rental.as_dict()
    rental_dict["due_date"] = rental.due_date.strftime("%Y-%m-%d")
    return make_response(rental_dict, 200)


def invalid_check_in_request_body(request_body):
    if "customer_id" not in request_body or "video_id" not in request_body:
        return True

    if not is_integer(request_body["video_id"]) or not is_integer(request_body["customer_id"]):
        return True

    if not Rental.query.get((request_body["customer_id"], request_body["video_id"])):
        return True
    return False


@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_body = request.get_json()

    if invalid_check_in_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    rental = Rental.query.get_or_404((request_body["customer_id"], request_body["video_id"]))

    db.session.delete(rental)
    rental_dict = rental.as_dict()
    db.session.commit()
    return make_response(rental_dict, 200)


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
