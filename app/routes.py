from flask import Blueprint, jsonify, request

from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental

from app import db
from datetime import datetime, timedelta, date
from sqlalchemy.orm import validates



customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
# ==============================HELPERS========================================


def err_404():
    """Helper function for 404 errors"""
    return "", 404


def validate_field(field, dic):
    if (field not in dic or dic[field] is None):
        return False
    else:
        return True


def id_int_validation(field, dic):
    if not isinstance(dic[field], int):
        return False
    return True


def customer_validation(post_request):
    valid = True
    valid &= validate_field("name", post_request)
    valid &= validate_field("postal_code", post_request)
    valid &= validate_field("phone", post_request)
    # valid &= "completed_at" in post_request
    return valid


def video_validation(post_request):
    valid = True
    valid &= validate_field("title", post_request)
    valid &= validate_field("release_date", post_request)
    valid &= validate_field("total_inventory", post_request)
    # valid &= validate_field("available_inventory", post_request)
    return valid




#==============================CUSTOMER_ROUTES==================================


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def check_all_customers():
    current_customers = Customer.query.all()
    customers_list = [client.customers_json_format() for client in current_customers]

    return jsonify(customers_list)


@customers_bp.route("/<client_id>", methods=["GET"], strict_slashes=False)
def find_customer(client_id):
    registered = Customer.query.get(client_id)
    if not registered:
        return err_404()

    return jsonify(registered.customers_json_format())


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def add_customer():
    customer_to_add = request.get_json()
    validation = customer_validation(customer_to_add)

    if not validation:
        return {"details": "Invalid data"}, 400

    new_customer = Customer(
        name=customer_to_add["name"], 
        postal_code=customer_to_add["postal_code"], 
        phone=customer_to_add["phone"]
        )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.client_id}), 201


@customers_bp.route("/<client_id>", methods=["PUT"], strict_slashes=False)
def update_customer(client_id):
    current_customer = Customer.query.get(client_id)
    if not current_customer:
        return err_404()

    customer_updates = request.get_json()
    valid_record = customer_validation(customer_updates)
    if not valid_record:
        return {"details": "Invalid data"}, 400

    current_customer.name = customer_updates["name"]
    current_customer.postal_code = customer_updates["postal_code"]
    current_customer.phone = customer_updates["phone"]
    db.session.commit()

    return jsonify(current_customer.customers_json_format())


@customers_bp.route("/<client_id>", methods=["DELETE"], strict_slashes=False)
def cancel_subscription(client_id):
    current_subscription = Customer.query.get(client_id)

    if not current_subscription:
        return err_404()

    db.session.delete(current_subscription)
    db.session.commit()
    return jsonify({"id": current_subscription.client_id})
    # return jsonify({"details": f"Subscription #{current_subscription.client_id}successfully deleted. We hope you change your mind."})


# ==============================VIDEO_ROUTES=====================================

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def check_inventory():
    current_videos = Video.query.all()
    videos_list = [t.videos_to_json_format() for t in current_videos]

    return jsonify(videos_list)


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def find_video(video_id):
    available_video = Video.query.get(video_id)
    if not available_video:
        return err_404()
    return jsonify(available_video.videos_to_json_format())


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def add_video():
    video_to_add = request.get_json()

    validation = video_validation(video_to_add)

    if not validation:
        return {"details": "Invalid data"}, 400

    new_video = Video(
        title=video_to_add["title"],
        release_date=video_to_add["release_date"],
        total_inventory=video_to_add["total_inventory"],
        available_inventory=video_to_add["total_inventory"]
        )

    db.session.add(new_video)
    db.session.commit()
    
    return jsonify({"id": new_video.video_id}), 201


@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video_to_update = request.get_json()
    old_video = Video.query.get(video_id)

    if not old_video:
        return err_404()

    valid_update = video_validation(video_to_update)
    if not valid_update:
        return {"details": "Invalid data"}, 400

    old_video.title = video_to_update["title"]
    old_video.release_date = video_to_update["release_date"]
    old_video.total_inventory = video_to_update["total_inventory"]

    db.session.commit()

    return jsonify(old_video.videos_to_json_format())


@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def discard_video(video_id):
    video_to_discard = Video.query.get(video_id)

    if not video_to_discard:
        return err_404()

    db.session.delete(video_to_discard)
    db.session.commit()
    return jsonify({"id": video_to_discard.video_id})



#===========================RELATIONSHIPS===========================#

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def rentals_check_out():
    rental_request = request.get_json()
    valid_customer_id = id_int_validation("customer_id", rental_request)
    valid_video_id = id_int_validation("video_id", rental_request)
    
    if not (valid_customer_id and valid_video_id):
        return {"details": "Invalid data"}, 400

    valid_customer = Customer.query.get(rental_request["customer_id"])
    valid_video = Video.query.get(rental_request["video_id"])

    if not (valid_customer and valid_video):
        return err_404()

    if valid_video.available_inventory is None or valid_video.available_inventory < 1:
        return {"details": "Invalid data"}, 400

    valid_video.available_inventory -= 1   # change nullable and default?
    valid_customer.videos_checked_out_count += 1

    new_rental = Rental(
        customer_id=rental_request["customer_id"], 
        vhs_id=rental_request["video_id"],
        due_date=date.today()+timedelta(days=7)
        )

    db.session.add(new_rental)
    db.session.commit()

    return jsonify(new_rental.rental_to_json_format())


@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def rentals_check_in():
    check_in = request.get_json()

    valid_customer_id = id_int_validation("customer_id", check_in)
    valid_video_id = id_int_validation("video_id", check_in)

    if not (valid_customer_id and valid_video_id):
        return {"details": "Invalid data"}, 400

    valid_customer = Customer.query.get(check_in["customer_id"])
    valid_video = Video.query.get(check_in["video_id"])
    if not (valid_video and valid_customer):
        return {"details": "Invalid data"}, 400


    current_rental = Rental.query.filter(Rental.vhs_id==check_in["video_id"], Rental.customer_id==check_in["customer_id"]).order_by(Rental.due_date.asc()).first()

    if current_rental is None:
        return {"details": "Invalid data"}, 400

    valid_video.available_inventory += 1   # change nullable and default?
    valid_customer.videos_checked_out_count -= 1

    db.session.delete(current_rental)
    db.session.commit()

    return jsonify(current_rental.check_in_json_format())


#==========================================================================

@customers_bp.route("/<client_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_rentals(client_id):
    customer = Customer.query.get(client_id)
    if customer is None:
        return err_404()
    rentals = Rental.query.filter(Rental.customer_id == customer.client_id).all()

    if rentals is None or len(rentals) == 0:
        return {}

    rental_list = [r.get_customer_rental_json() for r in rentals]

    return jsonify(rental_list)


@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_video_rentals(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return err_404()
    rentals = Rental.query.filter(Rental.vhs_id == video.video_id).all()

    if rentals is None or len(rentals) == 0:
        return {}

    rental_list = [r.get_video_rental_json() for r in rentals]

    return jsonify(rental_list)