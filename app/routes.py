from flask import Blueprint, request
from app.models.customer import Customer
from app.models.video import Video
from app.models.rentals import Rental
from flask.json import jsonify
from app import db

#2do2night:
#need to make .env file again
#need to register blueprints etc
#install pip? flask, postgres
#results = db.session.query(Foo, Bar, FooBarJoin).join(Foo, Foo.id==FooBarJoin.foo_id)\
#            .join(Bar, Bar.id==FooBarJoin.bar_id).filter(Foo.id == X).all()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


# GET /customers
# GET /customers/<id>
# POST /customers
# PUT /customers/<id>
# DELETE /customers/<id>
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():

@customers_bp.route("/<int:customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def new_customer():

@customers_bp.route("/<int:customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

@customers_bp.route("/<int:customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):

# GET /videos
# GET /vidoes/<id>
# POST /videos
# PUT /videos/<id>
# DELETE /videos/<id>
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
     if "title", "release_date", "total_inventory" in request_body: #probs wrong syntax tho
        video = Video(**request_body) #dict witchcraft
        db.session.add(video)
        db.session.commit()
        return jsonify(video.video_info()), 201
    return jsonify({"details": "Invalid data"}), 400

@videos_bp.route("/<int:video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    request_body = request.get_json()
    video = Video.query.get_or_404(video_id)
    if "title", "release_date", "total_inventory" in request_body: #probs wrong syntax tho
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.video_info()), 200
    else:
        return jsonify({"details": "Invalid data"}), 400

@video_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    vid = Video.query.get_or_404(video_id)
    db.session.delete(vid)
    db.session.commit()
    return make_response({"id": vid.video_id}, 200)

#POST /rentals/check-out
#POST /rentals/check-in
#GET /customers/<id>/rentals foobar?
#GET /videos/<id>/rentals foobar?
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return None

@rental_bp.route("/check-out", methods= ["POST"], strict_slashes=False)
def rent_video():
    request_body = request.get_json()
    checkem_out = request_body["customer_id"]
    check_video = request_body["video_id"]
    if not is_int(checkem_out) or not is_int(check_video):
        return make_response({"details": "Invalid ID"}, 400)

    customer = Customer.query.get_or_404(checkem_out)
    video = Video.query.get_or_404(video_check)
    this_rental = Rental(**request_body) #witchcraft, make sure can use outside of function headers again
    if video.available_inventory > 0:
        video.available_inventory -= 1 #use method in class 
        customer.videos_rented += 1 #use method in class 
        db.session.add(this_rental)
        db.session.commit()
        return make_response(this_rental.rental_info(), 200)
    return make_response({"details": "Inventory not available"}, 400)

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_video():
    request_body = request.get_json()
    checkin_customer = request_body["customer_id"]
    checkin_video = request_body["video_id"]
    if not is_int(checkin_customer) or not is_int(checkin_video):
        return make_response({"details": "Invalid ID"}, 400)
    this_rental = Rental.query.get_or_404((checkin_customer, checkin_video))
    if this_rental.customer.videos_rented > 0:
        this_rental.video.available_inventory += 1 #use method in class
        this_rental.customer.videos_rented -= 1 #use method in class
        db.session.commit()
        user_msg = this_rental.rental_info()
        del user_msg["due_date"]
        return make_response(user_msg, 200)
    return make_response({"details": "Rentals all returned"}, 400)

@customers_bp.route("/<int:customer_id>/rentals", methods=["GET"], strict_slashes=False)
def customer_rentals(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    rentals_history = []
    for rental in customer.videos: #<-is this relationship/ attribute correct?
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



