from flask import Blueprint, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app.models.rentals import Rental
from flask.json import jsonify
from app import db


#write tests? I can dream
#results = db.session.query(Foo, Bar, FooBarJoin).join(Foo, Foo.id==FooBarJoin.foo_id)\
#            .join(Bar, Bar.id==FooBarJoin.bar_id).filter(Foo.id == X).all()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    movie_buffs = Customer.query.all()
    response_body = []
    for nerd in movie_buffs:
        response_body.append(nerd.customer_info())
    return jsonify(response_body), 200

@customers_bp.route("/<int:customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.customer_info()), 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def new_customer():
    request_body = request.get_json()
    if "name" in request_body and "postal_code" in request_body and "phone" in request_body: 
        customer = Customer(**request_body)
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.customer_info()), 201
    else:
        return jsonify({"details": "Invalid data"}), 400

@customers_bp.route("/<int:customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    request_body = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    if "name" in request_body and "postal_code" in request_body and "phone" in request_body: 
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()
        return jsonify(customer.customer_info()), 200
    else:
        return jsonify({"details": "Invalid data"}), 400

@customers_bp.route("/<int:customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    keep_your_money = Customer.query.get_or_404(customer_id)
    db.session.delete(keep_your_money)
    db.session.commit()
    return make_response({"id": keep_your_money.customer_id}, 200)

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():
    videos = Video.query.all()
    response_body = []
    for video in videos:
        response_body.append(video.video_info())
    return jsonify(response_body), 200

@videos_bp.route("/<int:video_id>", methods=["GET"], strict_slashes=False)
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    return jsonify(video.video_info()), 200

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def post_video():
    request_body = request.get_json()
    if "title" in request_body and "release_date" in request_body and "total_inventory" in request_body: 
        video = Video(**request_body)
        video.available_inventory = video.total_inventory
        db.session.add(video)
        db.session.commit()
        return jsonify(video.video_info()), 201
    return jsonify({"details": "Invalid data"}), 400

@videos_bp.route("/<int:video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    request_body = request.get_json()
    video = Video.query.get_or_404(video_id)
    if "title" in request_body and "release_date" in request_body and "total_inventory" in request_body:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        video.available_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.video_info()), 200
    else:
        return jsonify({"details": "Invalid data"}), 400

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    vid = Video.query.get_or_404(video_id)
    db.session.delete(vid)
    db.session.commit()
    return make_response({"id": vid.video_id}, 200)

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return None

@rentals_bp.route("/check-out", methods= ["POST"], strict_slashes=False)
def rent_video():
    request_body = request.get_json()
    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    checkem_out = request_body["customer_id"]
    check_video = request_body["video_id"]
    if not is_int(checkem_out) or not is_int(check_video):
        return make_response({"details": "Bad request"}, 400)
    customer = Customer.query.get(checkem_out)
    video = Video.query.get(check_video)
    if not video.has_available_inventory(): 
        return make_response({"details": "Inventory not available"}, 400)
    video.check_out() 
    customer.videos_checked_out_count += 1
    this_rental = Rental(**request_body) 
    db.session.add(this_rental)
    db.session.commit()
    return make_response(this_rental.rental_info(), 200)
    

#all check in videos seem to be *not* passing
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_video():
    request_body = request.get_json()
    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    checkin_customer = request_body["customer_id"]
    checkin_video = request_body["video_id"]
    if not is_int(checkin_customer) or not is_int(checkin_video):
        return make_response({"details": "Bad request"}, 400)
    this_rental = Rental.query.filter_by(customer_id = checkin_customer, video_id = checkin_video).first()
    customer = Customer.query.get(checkin_customer)
    video = Video.query.get(checkin_video)
    this_customer = Customer.query.get(checkin_customer)
    if this_customer == None:
        return make_response({"details": "Invalid Customer"}, 400)

    if this_customer.videos_checked_out_count > 0:
        video.check_in()
        #this_rental.video.available_inventory += 1 
        this_customer.videos_checked_out_count -= 1 
        db.session.commit()
        user_msg = this_rental.rental_info()
        del user_msg["due_date"]
        return make_response(user_msg, 200)
    return make_response({"details": "Rentals all returned"}, 400)

@customers_bp.route("/<int:customer_id>/rentals", methods=["GET"], strict_slashes=False)
def customer_rentals(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    rentals_history = []
    for rental in customer.rentals:
        video = Video.query.get(rental.video_id)
        rentals_history.append({"release_date" : video.release_date,
                            "title" : video.title,
                            "due_date" : rental.due_date
                            })
    return jsonify(rentals_history), 200


@videos_bp.route("/<int:video_id>/rentals", methods=["GET"], strict_slashes=False)
def video_rentals(video_id):
    video = Video.query.get_or_404(video_id)
    rentals_history = []
    for rental in video.rentals:
        customer = Customer.query.get(rental.customer_id)
        rentals_history.append({"name" : customer.name,
                            "phone" : customer.phone,
                            "postal_code" : customer.postal_code,
                            "due_date" : rental.due_date
                            })
    return jsonify(rentals_history), 200



