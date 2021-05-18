from flask import Blueprint, request, make_response
from app import db
from .models.customer import Customer
from .models.video import Video
from flask import jsonify
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customers_bp.route("", methods=["GET"])
def get_customer():
    customers = Customer.query.all()

    customers_response = [customer.to_json() for customer in customers]

    return jsonify(customers_response), 200


@customers_bp.route("", methods=["POST"])
def add_customer():
    request_body = request.get_json()
    name = request_body.get("name")
    postal_code = request_body.get("postal_code")
    phone = request_body.get("phone")

    if not name or not postal_code or not phone:
        return jsonify({"details": "Invalid data"}), 400

    new_customer = Customer(name=name,
                            postal_code=postal_code,
                            phone=phone,
                            registered_at=datetime.now().strftime("%a, %d %b %Y, %H:%M:%S"))
    
    db.session.add(new_customer)
    db.session.commit()

    # id = request_body.get("id")
    # print("***", re)

    # return jsonify(new_customer.to_json()), 201
    return jsonify({"id": new_customer.id}), 201


@customers_bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def handle_customers(id):
    customer = Customer.query.get(id)

    if customer is None:
        return make_response("Not Found", 404)

    if request.method == "GET":
        return jsonify(customer.to_json()), 200
        # return jsonify({"id": customer.id,
        #         "name": customer.name,
        #         "phone": customer.phone,
        #         "postal_code": customer.postal_code,
        #         "registered_at": customer.registered_at,
        #         "videos_checked_out_count": customer.videos_checked_out_count}), 200

    elif request.method == "PUT":
        request_body = request.get_json()

        if not request_body.get("name") or not request_body.get("postal_code") or not request_body.get("phone"):
            return jsonify({"details": "Invalid data"}), 400

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        customer.registered_at = datetime.now().strftime("%a, %d %b %Y, %H:%M:%S")

        db.session.commit()

        return jsonify(customer.to_json()), 200
        # return jsonify({"id": customer.id,
        #                 "name": customer.name,
        #                 "phone": customer.phone,
        #                 "postal_code": customer.postal_code,
        #                 "registered_at": customer.registered_at,
        #                 "videos_checked_out_count": customer.videos_checked_out_count}), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return jsonify({"id": customer.id})


@videos_bp.route("", methods=["GET"])
def get_video():
    videos = Video.query.all()

    videos_response = [video.to_json() for video in videos]

    return jsonify(videos_response), 200


@videos_bp.route("", methods=["POST"])
def add_video():
    request_body = request.get_json()
    
    title = request_body.get("title")
    release_date = request_body.get("release_date")
    total_inventory = request_body.get("total_inventory")

    if not title or not release_date or not total_inventory:
        return jsonify({"details": ["title must be provided and it must be a string",
                                "total_inventory must be provided and it must be a number"]}), 400

    new_video = Video(title=title,
                    release_date=release_date,
                    total_inventory=total_inventory)

    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_json()), 201


@videos_bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def handle_videos(id):
    video = Video.query.get(id)

    if video is None:
        return make_response("Not Found"), 404

    if request.method == "GET":
        return jsonify(video.to_json()), 200

    if request.method == "PUT":
        request_body = request.get_json()

        if not request_body.get("title") or not request_body.get("release_date") or not request_body.get("total_inventory"):
            return make_response("Bad Request"), 400

        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

        db.session.commit()

        return jsonify(video.to_json()), 200

    if request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({"id": id}), 200





