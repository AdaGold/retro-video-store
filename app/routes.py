from flask import Blueprint, request, make_response
from app import db
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from flask import jsonify
from datetime import datetime, timedelta, date

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


def not_found():
    return make_response("Not Found", 404)


def customer_not_found(func):
    def inner(id):
        if Customer.query.get(id) is None:
            return make_response("Not Found", 404)
        return func(id)
    inner.__name__ = func.__name__
    return inner

def video_not_found(func):
    def inner(id):
        if Video.query.get(id) is None:
            return make_response("Not Found", 404)
        return func(id)
    inner.__name__ = func.__name__
    return inner

def handle_invalid_customer_data(func):
    def inner(*args, **kwargs):
        request_body = request.get_json()
        if not request_body.get("name") or not request_body.get("postal_code") or \
            not request_body.get("phone"):
            return jsonify({"details": "Invalid data"}), 400
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner

def handle_invalid_video_data(func):
    def inner(*args, **kwargs):
        request_body = request.get_json()
        if not request_body.get("title") or not request_body.get("release_date") or \
            not request_body.get("total_inventory"):
            return jsonify({"details": "Invalid data"}), 400
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner



@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    customers_response = [customer.to_json() for customer in customers]

    return jsonify(customers_response), 200


@customers_bp.route("", methods=["POST"])
@handle_invalid_customer_data
def add_customer():
    request_body = request.get_json()

    new_customer = Customer(name=request_body.get("name"),
                            postal_code=request_body.get("postal_code"),
                            phone=request_body.get("phone"),
                            registered_at=datetime.now().strftime("%a, %d %b %Y, %H:%M:%S"),
                            videos_checked_out_count=0)
    
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.id}), 201


@customers_bp.route("/<int:id>", methods=["GET"])
@customer_not_found
def get_customer(id):
    customer = Customer.query.get(id)

    return jsonify(customer.to_json()), 200


@customers_bp.route("/<int:id>", methods=["PUT"])
@customer_not_found
@handle_invalid_customer_data
def update_customer(id):
    customer = Customer.query.get(id)

    request_body = request.get_json()

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    customer.registered_at = datetime.now().strftime("%a, %d %b %Y, %H:%M:%S")

    db.session.commit()

    return jsonify(customer.to_json()), 200


@customers_bp.route("/<int:id>", methods=["DELETE"])
@customer_not_found
def delete_customer(id):
    customer = Customer.query.get(id)
    
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id})


@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()

    videos_response = [video.to_json() for video in videos]

    return jsonify(videos_response), 200


@videos_bp.route("", methods=["POST"])
@handle_invalid_video_data
def add_video():
    request_body = request.get_json()

    new_video = Video(title=request_body.get("title"),
                    release_date=request_body.get("release_date"),
                    total_inventory=request_body.get("total_inventory"),
                    available_inventory=request_body.get("total_inventory"))

    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_json()), 201


@videos_bp.route("/<int:id>", methods=["GET"])
@video_not_found
def get_video(id):
    video = Video.query.get(id)

    return jsonify(video.to_json()), 200


@videos_bp.route("/<int:id>", methods=["PUT"])
@video_not_found
@handle_invalid_video_data
def update_videos(id):
    video = Video.query.get(id)

    request_body = request.get_json()

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()

    return jsonify(video.to_json()), 200


@videos_bp.route("/<int:id>", methods=["DELETE"])
@video_not_found
def delete_video(id):
    video = Video.query.get(id)

    db.session.delete(video)
    db.session.commit()

    return jsonify({"id": id}), 200


@rentals_bp.route("/check-out", methods=["POST"])
@customer_not_found
@video_not_found
def handle_rentals_out():
    request_body = request.get_json()

    video_id = request_body.get("video_id")
    customer_id = request_body.get("customer_id")

    if type(customer_id) != int or type(video_id) != int:
        return invalid_data()

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    # results = db.session.query(Customer, Video, Rental).join(Customer, Customer.id==Rental.customer_id)\
    #     .join(Video, Video.id==Rental.video_id).filter(Customer.id == customer_id).all()
    # print("*** rental ", results)

    if video.available_inventory <= 0:
        return invalid_data()

    new_rental = Rental(customer_id=customer_id, 
                        video_id=video_id,
                        due_date = date.today() + timedelta(days=7),
                        status = "checked-out")
    
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    
    db.session.add(new_rental)
    db.session.commit()

    return jsonify({"customer_id": new_rental.customer_id,
                    "video_id": new_rental.video_id,
                    "due_date": new_rental.due_date,
                    "videos_checked_out_count": customer.videos_checked_out_count,
                    "available_inventory": video.available_inventory}), 200


@rentals_bp.route("/check-in", methods=["POST"])
@customer_not_found
@video_not_found
def handle_rentals_in():
    request_body = request.get_json()

    video_id = request_body.get("video_id")
    customer_id = request_body.get("customer_id")

    if type(customer_id) != int or type(video_id) != int:
        return invalid_data()

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    # results = db.session.query(Customer, Video, Rental).join(Customer, Customer.id==Rental.customer_id)\
    #     .join(Video, Video.id==Rental.video_id).filter(Customer.id == customer_id).all()
    # print("*** results ", results)

    for rental in customer.video:
        if rental.status == "checked-in":
            return make_response({400: "Bad Request"}, 400)
        if rental.video_id == video_id:
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1
            rental.status = "checked-in"
            # db.session.delete(rental)

    db.session.commit()
    
    return jsonify({"customer_id": customer_id,
                    "video_id": video_id,
                    "videos_checked_out_count": customer.videos_checked_out_count,
                    "available_inventory": video.available_inventory}), 200



@customers_bp.route("<int:id>/rentals", methods=["GET"])
@customer_not_found
def get_customer_rentals(id):
    customer = Customer.query.get(id)

    rental_response = []
    for rental in customer.video:
        video = Video.query.get(rental.video_id)
        
        rental_response.append({"release_date": video.release_date,
                                "title": video.title,
                                "due_date": rental.due_date})

    return jsonify(rental_response), 200


@videos_bp.route("<int:id>/rentals", methods=["GET"])
@video_not_found
def get_video_rentals(id):
    video = Video.query.get(id)

    rental_response = []
    for rental in video.customer:
        customer = Customer.query.get(rental.customer_id)

        rental_response.append({"due_date": rental.due_date,
                                "name": customer.name,
                                "phone": customer.phone,
                                "postal_code": customer.postal_code})

    return jsonify(rental_response), 200









