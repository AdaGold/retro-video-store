from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime



customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customer_bp.route("", methods=["POST"])
def valid_customer():

    form_data = request.get_json()
    if "name" not in form_data\
        or "postal_code" not in form_data\
            or "phone" not in form_data:
        return make_response({"details":"Invalid data"}, 400)
    else:
        new_customer = Customer(name=form_data["name"],
                                postal_code=form_data["postal_code"],
                                phone=form_data["phone"])

    if new_customer:
        new_customer.registered_at = datetime.utcnow()
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}), 201


@customer_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.cust_dict())
    return jsonify(customers_response)


@customer_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return (customer.cust_dict())


@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    '''update single customer'''
    customer = Customer.query.get_or_404(customer_id) 

    form_data = request.get_json()
    if "name" not in form_data\
        or "postal_code" not in form_data\
            or "phone" not in form_data:
        return make_response({"details":"Invalid data"}, 400)
    
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    db.session.commit()
    return jsonify(customer.cust_dict()), 200

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer= Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return {"id": customer.customer_id}


@video_bp.route("", methods=["POST"])
def post_video():
    form_data = request.get_json()
    if "title" not in form_data\
        or "release_date" not in form_data\
            or "total_inventory" not in form_data:
        return make_response({"details":["Invalid data"]},400)
    else:
        new_video = Video(title = form_data["title"],
                            release_date = form_data["release_date"],
                            total_inventory = form_data["total_inventory"])
    
        db.session.add(new_video)
        db.session.commit()
        return {"id": new_video.video_id}, 201


@video_bp.route("", methods=["GET"])
def get_videos():
    videos= Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(video.vid_dict())
    return jsonify(video_response),200

@video_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    return make_response(video.vid_dict())

@video_bp.route("/<video_id>",methods=["PUT"])
def put_video(video_id):
    video = Video.query.get_or_404(video_id)
    form_data = request.get_json()
    if "title" not in form_data\
        or "release_date" not in form_data\
            or "total_inventory" not in form_data:
        return make_response({"details":"invalid data"},400)

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]
    db.session.commit()
    return jsonify(video.vid_dict()), 200

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return make_response({"id": video.video_id},200)


