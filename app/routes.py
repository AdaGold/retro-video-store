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

@videos_bp.route("/<int:video_id>", methods=["GET"], strict_slashes=False)
def get_video(video_id):

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def post_video():

@videos_bp.route("/<int:video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):

@video_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    vid = Video.query.get(video_id)

    db.session.delete(vid)
    db.session.commit()
    return make_response({"id": vid.video_id}, 200)

#POST /rentals/check-out
#POST /rentals/check-in
#GET /customers/<id>/rentals foobar?
#GET /videos/<id>/rentals foobar?
@rental_bp.route("/check-out", methods= ["POST"], strict_slashes=False)
def rent_video():
    request_body = request.get_json()

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_video():
    request_body = request.get_json()

@customers_bp.route("/<int:customer_id>/rentals", methods=["GET"], strict_slashes=False)
def customer_rentals(customer_id):

@videos_bp.route("/<int:video_id>/rentals", methods=["GET"], strict_slashes=False)
def video_rentals(video_id):



