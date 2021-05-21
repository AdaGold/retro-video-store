from flask import Blueprint, request, jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

######################## HELPER FUNCTIONS ######################## 

def invalid_registration_request(request_body):
    if (not request_body
            or "name" not in request_body
            or "postal_code" not in request_body
            or "phone" not in request_body):
        return True

def invalid_video_request(request_body):
    if (not request_body
            or "title" not in request_body
            or "release_date" not in request_body
            or "total_inventory" not in request_body):
        return True

######################## CUSTOMER ENDPOINTS ######################## 

@customers_bp.route("/", methods = ["POST"], strict_slashes=False)
def register_customer():
    request_body = request.get_json()
    if invalid_registration_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(id=new_customer.id), 201

@customers_bp.route("/", methods = ["GET"], strict_slashes=False)
def view_all_customers():
        customers = Customer.query.all()
        all_customers = [customer.to_json() for customer in customers]
        return jsonify(all_customers)

@customers_bp.route("/<int:customer_id>", methods = ["GET"], strict_slashes=False)
def view_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_json())

@customers_bp.route("/<int:customer_id>", methods = ["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify(id=customer.id)

@customers_bp.route("/<int:customer_id>", methods = ["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    request_body = request.get_json()
    if invalid_registration_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    customer.name=request_body["name"]
    customer.postal_code=request_body["postal_code"]
    customer.phone=request_body["phone"]
    db.session.commit()
    return jsonify(customer.to_json())

######################## VIDEO ENDPOINTS ######################## 

@videos_bp.route("/", methods = ["POST"], strict_slashes=False)
def register_video():
    request_body = request.get_json()
    if invalid_video_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"]) 
    db.session.add(new_video)
    db.session.commit()
    return jsonify(id=new_video.id), 201

@videos_bp.route("/", methods = ["GET"], strict_slashes=False)
def view_all_videos():
    videos = Video.query.all()
    all_videos = [video.to_json() for video in videos]
    return jsonify(all_videos)

@videos_bp.route("/<int:video_id>", methods = ["GET"], strict_slashes=False)
def view_video(video_id):
    video = Video.query.get_or_404(video_id)
    return jsonify(video.to_json())

@videos_bp.route("/<int:video_id>", methods = ["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify(id=video.id)

@videos_bp.route("/<int:video_id>", methods = ["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    request_body = request.get_json()
    if invalid_video_request(request_body):
        return jsonify(details=f"Invalid data"), 400
    video.title=request_body["title"]
    video.release_date=request_body["release_date"]
    video.total_inventory=request_body["total_inventory"]
    db.session.commit()
    return jsonify(video.to_json())